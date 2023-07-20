from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from main.utils import for_htmx, get_page_by_request
from treecomments.models import TreeComment

from .models import Submission, SubmissionForm, SubmissionUpvote


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


@for_htmx(use_block_from_params=True)
def submission(request, pk):
    item = Submission.objects.get(pk=pk)
    template = "submission.html"
    return TemplateResponse(
        request,
        template,
        {"article": item, "submission": item},
    )


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
