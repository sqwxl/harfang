from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse

from .models import User


def user(request, username):
    view_user = User.objects.get(username=username)
    return TemplateResponse(
        request,
        "user.html",
        {
            "view_user": view_user,
        },
    )


def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("auth:login"))
    else:
        return TemplateResponse(request, "login.html", {"login_form": AuthenticationForm(), "register_form": form})
