from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _

from app.comments.models import Comment
from app.posts.models import Post
from app.utils import get_page_by_request
from app.utils.htmx import for_htmx

from .forms import ProfileForm, UserForm
from .models import Profile, User


def create(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("login"))

    form = UserForm()
    return TemplateResponse(
        request,
        "users/create.html",
        {
            "form": form,
            "page_title": _("Register"),
        },
    )


def profile(request, username):
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
def profile_edit(request, username):
    form = ProfileForm()

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("users:profile", kwargs={"username": username})
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
def posts(request, username):
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
def comments(request, username):
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
