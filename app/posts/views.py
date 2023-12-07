from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.http import HttpResponseForbidden, HttpResponseRedirect
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


@for_htmx(use_block_from_params=True)
def top(request):
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
            "page_title": _("Top Posts"),
        },
    )


@for_htmx(use_block_from_params=True)
def latest(request):
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

    comments = post.comments.all()

    if request.user.is_authenticated:
        form = CommentForm(initial={"post": pk})
    else:
        form = None

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
    status = 200
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            status = 422
    else:
        form = PostForm()

    return TemplateResponse(
        request,
        "posts/submit.html",
        {
            "form": form,
            "page_title": _("Submit Post"),
            "submit_text": _("Submit"),
        },
        status=status,
    )


@login_required
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    status = 200

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            status = 422
    else:
        form = PostForm(instance=post)

    return TemplateResponse(
        request,
        "base_form.html",
        {"form": form, "page_title": _("Edit Post")},
        status=status,
    )


@login_required
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if (
        request.user != post.user
        and not request.user.is_staff
        and not request.user.is_moderator
    ):
        # TODO flash user
        return HttpResponseForbidden()

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
    status = 200
    try:
        # delete vote if already voted
        vote = post.votes.get(user=request.user)
        vote.delete()
    except PostVote.DoesNotExist:
        # create vote if not
        try:
            PostVote(
                user=request.user, post=post, submit_date=timezone.now()
            ).save()
            status = 201
        except ValidationError as e:
            return HttpResponseForbidden(e)

    post.refresh_from_db()

    return TemplateResponse(
        request, "partials/vote.html", {"item": post}, status=status
    )
