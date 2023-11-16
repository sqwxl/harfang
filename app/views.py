from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from app.comments.forms import CommentForm
from app.comments.models import Comment
from app.utils import get_page_by_request
from app.utils.htmx import for_htmx, getify, is_htmx

from .forms import PostForm, ProfileForm, UserCreationForm
from .models import CommentVote, Post, PostVote, Profile, User


# redirect 'home' view to posts_top
def home(_):
    return HttpResponseRedirect(reverse("top"))


@for_htmx(use_block_from_params=True)
def posts_top(request):
    range = request.GET.get("range", "day")
    # get annotated queryset with user's vote status
    if request.user.is_authenticated:
        posts = Post.objects.with_user_vote_status(request.user)
    else:
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
    if request.user.is_authenticated:
        posts = Post.objects.with_user_vote_status(request.user)
    else:
        posts = Post.objects.all()
    return TemplateResponse(
        request,
        "posts/feed.html",
        {
            "page_obj": get_page_by_request(request, posts.latest()),
            "page_title": "Latest Posts",
        },
    )


@login_required
@require_POST
def post_vote(request, pk):
    # TODO generalize to handle votes coming from elsewhere than the feed view
    post = get_object_or_404(Post, pk=pk)
    vote = post.votes.filter(user=request.user)
    if vote.exists():
        vote.delete()
        post.has_voted = False
    else:
        vote = PostVote(user=request.user, post=post, submit_date=timezone.now())
        vote.save()
        post.has_voted = True

    return TemplateResponse(request, "posts/fragments/feed_item.html", {"post": post})


@login_required
@require_POST
def comment_vote(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    vote = comment.votes.filter(user=request.user)
    if vote.exists():
        vote.delete()
        comment.has_voted = False
    else:
        vote = CommentVote(user=request.user, comment=comment, submit_date=timezone.now())
        vote.save()
        comment.has_voted = True

    return TemplateResponse(request, "comments/fragments/detail.html", {"comment": comment})


@for_htmx(use_block_from_params=True)
def posts_detail(request, pk):
    return _posts_detail(request, pk)


def _posts_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = None
    comments = post.comments.all().ordered_by_points()

    if request.user.is_authenticated:
        # annotate comments w user's vote status
        comments = comments.with_user_vote_status(request.user)

        form = CommentForm(initial={"post": post})

        if request.method == "POST":
            form = CommentForm(request.POST)
            print(form.errors)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.save()
            if is_htmx(request):
                return _posts_detail(getify(request), pk)

            return HttpResponseRedirect("")

    return TemplateResponse(
        request,
        "posts/detail.html",
        {
            "page_title": post.title,
            "post": post,
            "form": form,
            "comments": comments,
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
            "page_obj": get_page_by_request(request, Comment.objects.filter(user=view_user).order_by("-submit_date")),
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
