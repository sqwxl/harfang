from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse

from newsapp.models import Comment, CommentForm, NewsItem

from .utils import for_htmx


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

    comments = Comment.objects.filter(news_item=news_item)
    return TemplateResponse(
        request,
        "newsapp/article.html",
        {
            "article": news_item,
            "comments": comments,
            "comment_form": CommentForm(),
        },
    )


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


def upvote_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.votes += 1
    comment.save()
    # todo


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
