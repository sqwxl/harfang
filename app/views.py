from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from app.treecomments.models import TreeComment
from app.utils import get_page_by_request
from app.utils.htmx import for_htmx

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
        },
    )


@for_htmx(use_block_from_params=True)
def posts_latest(request):
    return TemplateResponse(
        request,
        "posts/feed.html",
        {
            "page_obj": get_page_by_request(request, Post.objects.all().latest()),
        },
    )


@for_htmx(use_block_from_params=True)
def posts_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return TemplateResponse(
        request,
        "posts/detail.html",
        {"post": post},
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
        },
    )


def user_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return TemplateResponse(
        request,
        "users/profile.html",
        {
            "profile": profile,
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

    return TemplateResponse(request, "users/profile_edit.html", {"form": form})


def user_create(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("login"))
    else:
        form = UserCreationForm()
    return TemplateResponse(request, "users/form.html", {"form": form})
