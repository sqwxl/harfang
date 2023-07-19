from typing import Literal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from main.utils import for_htmx, get_page_by_request
from news.models import Article, NewsSite, Submission, SubmissionForm, SubmissionUpvote
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
def submissions(request):
    timespan_arg = request.GET.get("range", "day")
    queryset = Submission.objects.only_healthy()  # type: ignore
    if timespan_arg == "day":
        queryset = queryset.daily()
    elif timespan_arg == "week":
        queryset = queryset.weekly()
    elif timespan_arg == "month":
        queryset = queryset.monthly()
    elif timespan_arg == "year":
        queryset = queryset.yearly()

    return TemplateResponse(
        request,
        "submissions.html",
        {
            "page_obj": get_page_by_request(request, queryset),
        },
    )


@for_htmx(use_block_from_params=True)
def submissions_new(request):
    return TemplateResponse(
        request,
        "submissions.html",
        {"page_obj": get_page_by_request(request, Submission.objects.new())},  # type: ignore
    )


def submissions_vote(request: HttpRequest, pk):
    submission = Submission.objects.get(pk=pk)
    try:
        vote = SubmissionUpvote.objects.get(user=request.user, submission=submission)
        vote.delete()
    except SubmissionUpvote.DoesNotExist:
        vote = SubmissionUpvote.objects.create(user=request.user, submission=submission)
        vote.save()
    return TemplateResponse(
        request,
        "includes/feed_item.html",
        {
            "item": submission,
            "item_url": reverse("news:submission", kwargs={"pk": submission.pk}),
            "vote_url": reverse("news:submissions_vote", kwargs={"pk": submission.pk}),
        },
    )


def item_view(request, item_type: Literal["article", "submission"], pk):
    if item_type == "article":
        item = Article.objects.get(pk=pk)
        template = "article.html"
    else:
        item = Submission.objects.get(pk=pk)
        template = "submission.html"

    return TemplateResponse(
        request,
        template,
        {"article": item, "submission": item},
    )


@for_htmx(use_block_from_params=True)
def article(request, pk):
    return item_view(request, "article", pk)


@for_htmx(use_block_from_params=True)
def submission(request, pk):
    return item_view(request, "submission", pk)


def submission_form(request):
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            return HttpResponseRedirect(reverse("news:submission", args=(submission.pk,)))
    else:
        form = SubmissionForm()

    return TemplateResponse(
        request,
        "submission_form.html",
        {
            "form": form,
        },
    )


def about(request):
    return TemplateResponse(request, "about.html")


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
def user_submissions(request, username):
    view_user = User.objects.get(username=username)
    return TemplateResponse(
        request,
        "submissions.html",
        {
            "view_user": view_user,
            "page_obj": get_page_by_request(request, Submission.objects.filter(user=view_user).order_by("-created_on")),
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
