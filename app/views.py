from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from app.comments.models import Comment
from app.utils import get_page_by_request
from app.utils.htmx import for_htmx

from .models import Post, PostForm


# redirect 'home' view to posts_top
def home(_):
    return HttpResponseRedirect(reverse("top"))


@for_htmx(use_block_from_params=True)
def posts_top(request):
    timespan_arg = request.GET.get("range", "day")
    queryset = Post.objects.only_healthy()  # type: ignore
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
def posts_latest(request):
    return TemplateResponse(
        request,
        "submissions.html",
        {"page_obj": get_page_by_request(request, Post.objects.new())},  # type: ignore
    )


def submissions_vote(request: HttpRequest, pk):
    post = Post.objects.get(pk=pk)
    # try:
    #     vote = SubmissionUpvote.objects.get(user=request.user, post=post)
    #     vote.delete()
    # except SubmissionUpvote.DoesNotExist:
    #     vote = SubmissionUpvote.objects.create(user=request.user, post=post)
    #     vote.save()
    return TemplateResponse(
        request,
        "fragments/feed_item.html",
        {
            "item": post,
            "item_url": post.get_absolute_url(),
            # "vote_url": reverse("news:submissions_vote", kwargs={"pk": post.pk}), TODO
        },
    )


@for_htmx(use_block_from_params=True)
def posts_detail(request, pk):
    item = Post.objects.get(pk=pk)
    template = "post.html"
    return TemplateResponse(
        request,
        template,
        {"article": item, "post": item},
    )


def posts_submit(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostForm()

    return TemplateResponse(
        request,
        "submission_form.html",
        {
            "form": form,
        },
    )


@for_htmx(use_block_from_params=True)
def user_posts(request, username):
    view_user = User.objects.get(username=username)
    return TemplateResponse(
        request,
        "posts/list.html",
        {
            "view_user": view_user,
            "page_obj": get_page_by_request(request, Post.objects.filter(user=view_user).order_by("-created_on")),
        },
    )


@for_htmx(use_block_from_params=True)
def user_comments(request, username):
    view_user = get_object_or_404(User, username=username)
    return TemplateResponse(
        request,
        "users/comments.html",
        {
            "view_user": view_user,
            "page_obj": get_page_by_request(request, Comment.objects.filter(user=view_user).order_by("-created_on")),
        },
    )


def user_detail(request, username):
    view_user = User.objects.get(username=username)
    return TemplateResponse(
        request,
        "users/detail.html",
        {
            "view_user": view_user,
        },
    )


def user_create(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("auth:login"))
    else:
        return TemplateResponse(request, "auth/login.html", {"login_form": AuthenticationForm(), "register_form": form})
