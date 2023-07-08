from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from newsapp.models import Comment, CommentForm, NewsItem

from .utils import for_htmx, is_htmx


def get_page_by_request(request, queryset, paginate_by=10):
    return Paginator(queryset, per_page=paginate_by).get_page(request.GET.get("page"))


@for_htmx(use_block_from_params=True)
def index(request):
    return TemplateResponse(
        request,
        "newsapp/index.html",
        {
            "page_obj": get_page_by_request(request, NewsItem.objects.all().order_by("-pub_date")),
        },
    )


@for_htmx(use_block_from_params=True)
def article(request, pk):
    news_item = NewsItem.objects.get(pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news_item = news_item
            comment.user = request.user
            comment.save()
    else:
        comment_form = CommentForm()

    comments = news_item.comments.all()  # type: ignore
    return TemplateResponse(
        request,
        "newsapp/article.html",
        {
            "article": news_item,
            "comments": comments,
            "comment_form": CommentForm(),
        },
    )


@for_htmx(use_block_from_params=True)
def reply(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == "POST":
        reply = CommentForm(request.POST)
        if reply.is_valid():
            reply = reply.save(commit=False)
            reply.news_item = comment.news_item
            reply.parent = comment
            reply.user = request.user
            reply.save()
            return HttpResponseRedirect(reverse("newsapp:article", args=(comment.news_item.pk,)))
    else:
        reply = CommentForm()
    return TemplateResponse(
        request,
        "newsapp/reply.html",
        {
            "comment": comment,
            "form": reply,
        },
    )


@require_http_methods(["DELETE"])
def comment_delete(request: HttpRequest, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == "DELETE":
        comment.text = "[deleted]"
        comment.deleted = True
        comment.deleted_on = timezone.now()
        comment.deleded_by = request.user
        comment.save()
    if is_htmx(request):
        return TemplateResponse(
            request,
            "newsapp/comment.html",
            {
                "comment": comment,
            },
        )
    else:
        return HttpResponseRedirect(reverse("newsapp:article", args=(comment.news_item.pk,)))


def comment(request: HttpRequest, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return HttpResponseRedirect(reverse("newsapp:article", args=(comment.news_item.pk,)))
    elif request.method == "PUT":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.edited_on = timezone.now()
            comment.save()
            return HttpResponseRedirect(reverse("newsapp:article", args=(comment.news_item.pk,)))
    elif request.method == "DELETE":
        return comment_delete(request, pk)

    form = CommentForm(instance=comment)
    return TemplateResponse(
        request,
        "newsapp/comment-edit.html",
        {
            "form": form,
        },
    )


def about(request):
    return TemplateResponse(request, "newsapp/about.html")


def login_view(request):
    if request.method == "POST":
        if "register" in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("newsapp:index"))
            else:
                return TemplateResponse(
                    request, "newsapp/login.html", {"login_form": AuthenticationForm(), "register_form": form}
                )

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("newsapp:index"))
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
    return HttpResponseRedirect(reverse("newsapp:index"))


def forgot(request):
    if request.method == "POST":
        # todo
        ...
    return TemplateResponse(request, "newsapp/forgot.html", {"form": PasswordResetForm()})
