from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from app.comments.forms import CommentForm
from app.utils import get_page_by_request
from app.utils.htmx import for_htmx

from .forms import PostForm
from .models import Post, PostVote


# redirect 'home' view to posts_top
def home(_):
    return HttpResponseRedirect(reverse("posts:top"))


@for_htmx(use_block_from_params=True)
def top(request):
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
def latest(request):
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


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user.is_authenticated:
        form = CommentForm(initial={"post": pk})
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
def create(request):
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
        "posts/create.html",
        {
            "form": form,
            "page_title": _("Submit Post"),
        },
    )


@login_required
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post.get_absolute_url())

    return TemplateResponse(
        request, "posts/edit.html", {"form": form, "page_title": _("Edit Post")}
    )


@login_required
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if (
        request.user != post.user
        or not request.user.is_staff
        or not request.user.is_moderator
    ):
        # TODO flash user
        return HttpResponseRedirect(post.get_absolute_url())

    if request.method == "POST":
        post.delete()
        # TODO flash user
        return HttpResponseRedirect(reverse("home"))

    return TemplateResponse(
        request,
        "posts/delete.html",
        {"post": post, "page_title": _("Delete Post")},
    )


@login_required
@require_POST
def vote(request, pk):
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

    if request.htmx:
        return TemplateResponse(
            request,
            "partials/vote_form.html",
            {"item": post},
        )
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
