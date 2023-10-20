from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = auth.authenticate(
                request, username=form.cleaned_data["username"], password=form.cleaned_data["password"]
            )
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("news:news"))
            else:
                form.add_error(None, "Invalid username or password")
                return TemplateResponse(
                    request, "login.html", {"login_form": form, "register_form": UserCreationForm()}
                )
        else:
            return TemplateResponse(request, "login.html", {"login_form": form, "register_form": UserCreationForm()})

    return TemplateResponse(
        request, "login.html", {"login_form": AuthenticationForm(), "register_form": UserCreationForm()}
    )


def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("news:news"))


def forgot_view(request):
    if request.method == "POST":
        # todo
        ...
    return TemplateResponse(request, "forgot.html", {"form": PasswordResetForm()})
