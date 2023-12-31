from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _

from app.comments.models import Comment
from app.posts.models import Post
from app.utils import get_page

from .forms import ProfileForm, UserForm
from .models import Profile, User


def create(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("login"))
    else:
        form = UserForm()

    return TemplateResponse(
        request,
        "base_form.html",
        {
            "form": form,
            "page_title": _("Register"),
            "submit_text": _("Register"),
        },
    )


def profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return TemplateResponse(
        request,
        "users/profile.html",
        {
            "profile": profile,
            "page_title": str(profile),
        },
    )


@login_required
def profile_edit(request, username):
    form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("users:profile", kwargs={"username": username})
            )

    return TemplateResponse(
        request,
        "base_form.html",
        {
            "form": form,
            "page_title": _("Edit Profile"),
        },
    )


def posts(request, username):
    view_user = User.objects.get(username=username)
    return TemplateResponse(
        request,
        "users/posts.html",
        {
            "view_user": view_user,
            "page_obj": get_page(
                request,
                Post.objects.filter(user=view_user).order_by("-submit_date"),
            ),
            "page_title": _("{username}'s Posts").format(username=username),
        },
    )


def comments(request, username):
    view_user = get_object_or_404(User, username=username)
    return TemplateResponse(
        request,
        "users/comments.html",
        {
            "view_user": view_user,
            "page_obj": get_page(
                request,
                Comment.objects.filter(user=view_user).order_by("-submit_date"),
            ),
            "page_title": _("{username}'s Comments").format(username=username),
        },
    )
