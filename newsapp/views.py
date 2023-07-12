from typing import Literal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from newsapp.models import Article, Comment, CommentForm, Post, PostForm

from .utils import for_htmx, is_htmx


def get_page_by_request(request, queryset, paginate_by=10):
    return Paginator(queryset, per_page=paginate_by).get_page(request.GET.get("page"))


@for_htmx(use_block_from_params=True)
def news(request):
    return TemplateResponse(
        request,
        "newsapp/news.html",
        {
            "page_obj": get_page_by_request(request, Article.objects.all().order_by("-pub_date")),
        },
    )


@for_htmx(use_block_from_params=True)
def posts(request):
    return TemplateResponse(
        request,
        "newsapp/posts.html",
        {
            "page_obj": get_page_by_request(request, Post.objects.order_by("-created_on", "-votes")),
        },
    )


def item_view(request, item_type: Literal["article", "post"], pk):
    if item_type == "article":
        item = Article.objects.get(pk=pk)
        template = "newsapp/article.html"
    else:
        item = Post.objects.get(pk=pk)
        template = "newsapp/post.html"

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.content_object = item
            comment.user = request.user
            comment.save()
            form = CommentForm()
    else:
        form = CommentForm()

    return TemplateResponse(
        request,
        template,
        {
            "article": item,
            "post": item,
            "comments": item.comments.all(),  # type: ignore
            "comment_form": form,
        },
    )


@for_htmx(use_block_from_params=True)
def article(request, pk):
    return item_view(request, "article", pk)


@for_htmx(use_block_from_params=True)
def post(request, pk):
    return item_view(request, "post", pk)


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse("newsapp:post", args=(post.pk,)))
    else:
        form = PostForm()

    return TemplateResponse(
        request,
        "newsapp/post-new.html",
        {
            "form": form,
        },
    )


def reply(request, pk):
    parent = Comment.objects.get(pk=pk)
    if request.method == "POST":
        reply = CommentForm(request.POST)
        if reply.is_valid():
            reply = reply.save(commit=False)
            reply.content_object = parent.content_object
            reply.parent = parent
            reply.user = request.user
            reply.save()
            viewname = parent.content_object.__class__.__name__.lower()
            return HttpResponseRedirect(reverse(f"newsapp:{viewname}", args=(parent.post.pk,)))
    else:
        reply = CommentForm()

    return TemplateResponse(
        request,
        "newsapp/reply.html",
        {
            "comment": parent,
            "form": reply,
        },
    )


def comment(request: HttpRequest, article_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.edited_on = timezone.now()
            comment.edited_by = request.user
            comment.save()
            return HttpResponseRedirect(reverse("newsapp:article", args=(article_id,)))
    elif request.method == "DELETE":
        return comment_delete(request, comment_id)
    else:
        form = CommentForm(instance=comment)

    return TemplateResponse(
        request,
        "newsapp/comment-edit.html",
        {
            "comment": comment,
            "form": form,
        },
    )


@require_http_methods(["DELETE"])
def comment_delete(request: HttpRequest, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == "DELETE":
        comment.text = "[deleted]"
        comment.deleted_on = timezone.now()
        comment.deleded_by = request.user
        comment.save()
    if is_htmx(request):
        return TemplateResponse(
            request,
            "newsapp/comment.html",
            {
                "in_tree": True,
                "comment": comment,
            },
        )
    else:
        return HttpResponseRedirect(
            reverse(f"newsapp:{comment.content_object.__class__.__name__.lower()}", args=(comment.content_object.pk,))
        )


def about(request):
    return TemplateResponse(request, "newsapp/about.html")


@for_htmx(use_block_from_params=True)
def user(request, username, items="posts"):
    user = User.objects.get(username=username)
    if items == "posts":
        objects = Post.objects.filter(user=user).order_by("-created_on", "-votes")
    else:
        objects = Comment.objects.filter(user=user).order_by("-created_on")
    return TemplateResponse(
        request,
        "newsapp/user.html",
        {
            "user": user,
            "item_type": items,
            "page_obj": get_page_by_request(request, objects),
        },
    )


def login_view(request):
    if request.method == "POST":
        if "register" in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("newsapp:news"))
            else:
                return TemplateResponse(
                    request, "newsapp/login.html", {"login_form": AuthenticationForm(), "register_form": form}
                )

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("newsapp:news"))
            else:
                form.add_error(None, "Invalid username or password")
                return TemplateResponse(
                    request, "newsapp/login.html", {"login_form": form, "register_form": UserCreationForm()}
                )
        else:
            return TemplateResponse(
                request, "newsapp/login.html", {"login_form": form, "register_form": UserCreationForm()}
            )

    return TemplateResponse(
        request, "newsapp/login.html", {"login_form": AuthenticationForm(), "register_form": UserCreationForm()}
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("newsapp:news"))


def forgot(request):
    if request.method == "POST":
        # todo
        ...
    return TemplateResponse(request, "newsapp/forgot.html", {"form": PasswordResetForm()})
