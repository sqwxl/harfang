from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from app.treecomments.forms import TreeCommentForm
from app.treecomments.models import TreeComment
from app.utils import get_page_by_request
from app.utils.htmx import for_htmx, getify, is_htmx

from .forms import PostForm, ProfileForm, UserCreationForm
from .models import Post, Profile, User


# redirect 'home' view to posts_top
def home(_):
    return HttpResponseRedirect(reverse("top"))


@for_htmx(use_block_from_params=True)
def posts_top(request):
    range = request.GET.get("range", "day")
    posts = Post.objects.all()
    if range == "day":
        queryset = posts.day().top()
    elif range == "week":
        queryset = posts.week().top()
    elif range == "month":
        queryset = posts.month().top()
    elif range == "year":
        queryset = posts.year().top()
    else:  # i.e. "all"
        queryset = posts.top()

    return TemplateResponse(
        request,
        "posts/feed.html",
        {
            "page_obj": get_page_by_request(request, queryset),
            "range": range,
            "has_menu": True,
            "page_title": "Top Posts",
        },
    )


@for_htmx(use_block_from_params=True)
def posts_latest(request):
    return TemplateResponse(
        request,
        "posts/feed.html",
        {
            "page_obj": get_page_by_request(request, Post.objects.all().latest()),
            "page_title": "Latest Posts",
        },
    )


@for_htmx(use_block_from_params=True)
def posts_detail(request, pk):
    return _posts_detail(request, pk)


def _posts_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = None
    if request.user.is_authenticated:
        form = TreeCommentForm(post, initial={"user": request.user})

        if request.method == "POST":
            form = TreeCommentForm(post, request.POST)
            if form.is_valid():
                comment = form.get_comment_object()
                comment.user = request.user
                comment.content_object = post
                comment.save()
            if is_htmx(request):
                return _posts_detail(getify(request), pk)

            return HttpResponseRedirect("")

    return TemplateResponse(
        request,
        "posts/detail.html",
        {
            "post": post,
            "page_title": post.title,
            "form": form,
            "comments": post.comments.all(),
        },
    )


@login_required
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
        "posts/form.html",
        {
            "form": form,
            "page_title": "Submit Post",
        },
    )


def user_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return TemplateResponse(
        request,
        "users/profile.html",
        {
            "profile": profile,
            "page_title": profile.user.username,
        },
    )


@login_required
def user_profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("profile", kwargs={"username": request.user.username}))
    else:
        form = ProfileForm()

    return TemplateResponse(
        request,
        "users/profile_edit.html",
        {
            "form": form,
            "page_title": "Edit Profile",
        },
    )


@for_htmx(use_block_from_params=True)
def user_posts(request, username):
    view_user = User.objects.get(username=username)
    return TemplateResponse(
        request,
        "users/posts.html",
        {
            "view_user": view_user,
            "page_obj": get_page_by_request(request, Post.objects.filter(user=view_user).order_by("-submit_date")),
            "page_title": f"{view_user.username}'s Posts",
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
            "page_obj": get_page_by_request(
                request, TreeComment.objects.filter(user=view_user).order_by("-submit_date")
            ),
            "page_title": f"{view_user.username}'s Comments",
        },
    )


def user_create(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("login"))
    else:
        form = UserCreationForm()
    return TemplateResponse(request, "users/form.html", {"form": form})
