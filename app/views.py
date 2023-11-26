from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from app.comments.forms import CommentForm
from app.comments.models import Comment
from app.utils import get_page_by_request
from app.utils.htmx import for_htmx

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
            "page_title": _("Top Posts"),
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
            "page_title": _("Latest Posts"),
        },
    )


def posts_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user.is_authenticated:
        form = CommentForm(initial={"post": post})
        comments = post.comments.with_user_vote_status(request.user)
    else:
        form = None
        comments = post.comments.all()

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
            "page_title": _("Submit Post"),
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
def user_profile_edit(request, username):
    form = ProfileForm()

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("profile", kwargs={"username": username})
            )
    return TemplateResponse(
        request,
        "users/profile_edit.html",
        {
            "form": form,
            "page_title": _("Edit Profile"),
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
            "page_obj": get_page_by_request(
                request,
                Post.objects.filter(user=view_user).order_by("-submit_date"),
            ),
            "page_title": _("{username}'s Posts").format(username=username),
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
                request,
                Comment.objects.filter(user=view_user).order_by("-submit_date"),
            ),
            "page_title": _("{username}'s Comments").format(username=username),
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
    return TemplateResponse(
        request,
        "users/form.html",
        {
            "form": form,
            "page_title": _("Register"),
        },
    )


@login_required
@require_POST
def post_vote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    try:
        vote = post.votes.get(user=request.user)
        vote.delete()
        post.has_voted = False
    except PostVote.DoesNotExist:
        PostVote(
            user=request.user, post=post, submit_date=timezone.now()
        ).save()
        post.has_voted = True
    except PostVote.MultipleObjectsReturned as e:
        # TODO handle this case (should never happen since unique_together is set on PostVote)
        print(e)

    post.refresh_from_db()

    # TODO generalize to handle votes coming from elsewhere than the feed view
    return TemplateResponse(
        request, "posts/partials/feed_item.html", {"post": post}
    )


@login_required
@require_POST
def comment_vote(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    try:
        vote = comment.votes.get(user=request.user)
        vote.delete()
        comment.has_voted = False
    except CommentVote.DoesNotExist:
        CommentVote(
            user=request.user, comment=comment, submit_date=timezone.now()
        ).save()
        comment.has_voted = True
    except CommentVote.MultipleObjectsReturned as e:
        # TODO handle this case (should never happen since unique_together is set on CommentVote)
        print(e)

    comment.refresh_from_db()

    return TemplateResponse(
        request, "comments/detail.html", {"comment": comment}
    )
