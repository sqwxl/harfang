from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from app.forms import AppModelForm

from .models import Profile


class UserForm(UserCreationForm, AppModelForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")
        help_texts = {
            "email": _("Optional"),
        }


class ProfileForm(AppModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 5}),
        }
        help_texts = {
            "bio": _("Maximum {n} characters").format(
                n=settings.BIO_MAX_LENGTH
            ),
        }
