from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from app.forms import AppModelForm

from .models import Post


class PostForm(AppModelForm):
    class Meta:
        model = Post
        fields = ["title", "url", "body"]
        help_texts = {
            "title": _("Maximum {n} characters").format(
                n=settings.POST_TITLE_MAX_LENGTH
            ),
            "url": _("Maximum {n} characters").format(
                n=settings.POST_URL_MAX_LENGTH
            ),
            "body": _("Maximum {n} characters").format(
                n=settings.POST_BODY_MAX_LENGTH
            ),
        }
        widgets = {
            "body": forms.Textarea(),
        }
