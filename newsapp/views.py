from typing import Literal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from newsapp.models import (
    Article,
    ArticleComment,
    Comment,
    CommentForm,
    NewsSite,
    Submission,
    SubmissionComment,
    SubmissionForm,
    SubmissionUpvote,
)

from .utils import for_htmx, is_htmx


def get_page_by_request(request, queryset: QuerySet, paginate_by=10):
    return Paginator(queryset, per_page=paginate_by).get_page(request.GET.get("page"))


@for_htmx(use_block_from_params=True)
def news(request):
    return TemplateResponse(
        request,
        "newsapp/news.html",
        {
            "page_obj": get_page_by_request(request, Article.objects.all()),
        },
    )


@for_htmx(use_block_from_params=True)
def submissions(request):
    timespan_arg = request.GET.get("range", "day")
    queryset = Submission.objects.only_health().annotate_user_votes(request.user)  # type: ignore
    if timespan_arg == "day":
        queryset = queryset.top_daily()
    elif timespan_arg == "week":
        queryset = queryset.top_weekly()
    elif timespan_arg == "month":
        queryset = queryset.top_monthly()
    elif timespan_arg == "year":
        queryset = queryset.top_yearly()
    elif timespan_arg == "all":
        queryset = queryset.top_all_time()

    return TemplateResponse(
        request,
        "newsapp/submissions.html",
        {
            "page_obj": get_page_by_request(request, queryset),
        },
    )


@for_htmx(use_block_from_params=True)
def submissions_new(request):
    return TemplateResponse(
        request,
        "newsapp/submissions.html",
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
        "newsapp/includes/feed_item.html",
        {
            "item": submission,
            "item_url": reverse("newsapp:submission", kwargs={"pk": submission.pk}),
            "vote_url": reverse("newsapp:submissions_vote", kwargs={"pk": submission.pk}),
        },
    )


def item_view(request, item_type: Literal["article", "submission"], pk):
    if item_type == "article":
        item = Article.objects.get(pk=pk)
        template = "newsapp/article.html"
    else:
        item = Submission.objects.get(pk=pk)
        template = "newsapp/submission.html"

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment[item_type] = item
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
            "submission": item,
            "comments": item.comments.all(),  # type: ignore
            "comment_form": form,
        },
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
            return HttpResponseRedirect(reverse("newsapp:submission", args=(submission.pk,)))
    else:
        form = SubmissionForm()

    return TemplateResponse(
        request,
        "newsapp/submission_form.html",
        {
            "form": form,
        },
    )


def reply_article_comment(request, pk):
    parent = ArticleComment.objects.get(pk=pk)
    if request.method == "POST":
        reply = CommentForm(request.POST)
        if reply.is_valid():
            reply = reply.save(commit=False)
            reply.article = parent.article
            reply.parent = parent
            reply.user = request.user
            reply.save()
            viewname = parent.content_object.__class__.__name__.lower()
            return HttpResponseRedirect(reverse(f"newsapp:{viewname}", args=(parent.submission.pk,)))
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


def reply_submission_comment(request, pk):
    parent = SubmissionComment.objects.get(pk=pk)
    if request.method == "POST":
        reply = CommentForm(request.POST)
        if reply.is_valid():
            reply = reply.save(commit=False)
            # reply.article = parent.article TODO
            reply.parent = parent
            reply.user = request.user
            reply.save()
            viewname = parent.content_object.__class__.__name__.lower()
            return HttpResponseRedirect(reverse(f"newsapp:{viewname}", args=(parent.submission.pk,)))
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


def comment(request: HttpRequest, pk):
    comment = Comment.objects.get(pk=pk)
    item_type = comment.content_type.model_class()
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.edited_on = timezone.now()
            comment.edited_by = request.user
            comment.save()
            if item_type == Article:
                view = "newsapp:article"
            elif item_type == Submission:
                view = "newsapp:submission"
            else:
                raise ValueError(f"Unknown content type: {item_type}")
            return HttpResponseRedirect(reverse(view, args=(comment.content_object.id,)))
    elif request.method == "DELETE":
        return comment_delete(request, comment)
    else:
        form = CommentForm(instance=comment)

    return TemplateResponse(
        request,
        "newsapp/comment_edit.html",
        {
            "comment": comment,
            "form": form,
        },
    )


@require_http_methods(["DELETE"])
def comment_delete(request: HttpRequest, comment):
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


def news_site(request, pk):
    news_site = NewsSite.objects.get(pk=pk)
    return TemplateResponse(request, "newsapp/news_site.html", {"news_site": news_site})


def user(request, username):
    view_user = User.objects.get(username=username)
    return TemplateResponse(
        request,
        "newsapp/user.html",
        {
            "view_user": view_user,
        },
    )


@for_htmx(use_block_from_params=True)
def user_submissions(request, username):
    view_user = User.objects.get(username=username)
    return TemplateResponse(
        request,
        "newsapp/submissions.html",
        {
            "view_user": view_user,
            "page_obj": get_page_by_request(request, Submission.objects.filter(user=view_user).order_by("-created_on")),
        },
    )


@for_htmx(use_block_from_params=True)
def user_comments(request, username):
    view_user = User.objects.get(username=username)
    return TemplateResponse(
        request,
        "newsapp/comment_feed.html",
        {
            "view_user": view_user,
            "page_obj": get_page_by_request(request, Comment.objects.filter(user=view_user).order_by("-created_on")),
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
