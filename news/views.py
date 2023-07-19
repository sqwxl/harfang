from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from main.utils import for_htmx, get_page_by_request
from news.models import Article, NewsSite
from treecomments.models import TreeComment


@for_htmx(use_block_from_params=True)
def news(request):
    return TemplateResponse(
        request,
        "news.html",
        {
            "page_obj": get_page_by_request(request, Article.objects.all()),
        },
    )


@for_htmx(use_block_from_params=True)
def article(request, pk):
    item = Article.objects.get(pk=pk)
    template = "article.html"

    return TemplateResponse(
        request,
        template,
        {"article": item, "submission": item},
    )


def news_site(request, pk):
    news_site = NewsSite.objects.get(pk=pk)
    return TemplateResponse(request, "news_site.html", {"news_site": news_site})


def user(request, username):
    view_user = User.objects.get(username=username)
    return TemplateResponse(
        request,
        "user.html",
        {
            "view_user": view_user,
        },
    )


@for_htmx(use_block_from_params=True)
def user_comments(request, username):
    view_user = get_object_or_404(User, username=username)
    return TemplateResponse(
        request,
        "treecomments/list.html",
        {
            "view_user": view_user,
            "page_obj": get_page_by_request(
                request, TreeComment.objects.filter(user=view_user).order_by("-created_on")
            ),
        },
    )


def login_view(request):
    if request.method == "POST":
        if "register" in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("news:news"))
            else:
                return TemplateResponse(
                    request, "login.html", {"login_form": AuthenticationForm(), "register_form": form}
                )

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("news:news"))
            else:
                form.add_error(None, "Invalid username or password")
                return TemplateResponse(
                    request, "login.html", {"login_form": form, "register_form": UserCreationForm()}
                )
        else:
            return TemplateResponse(request, "login.html", {"login_form": form, "register_form": UserCreationForm()})

    return TemplateResponse(
        request, "login.html", {"login_form": AuthenticationForm(), "register_form": UserCreationForm()}
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("news:news"))


def forgot(request):
    if request.method == "POST":
        # todo
        ...
    return TemplateResponse(request, "forgot.html", {"form": PasswordResetForm()})
