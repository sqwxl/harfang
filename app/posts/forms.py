from django import forms
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from app.forms import AppModelForm

from .models import Post


class PostForm(AppModelForm):
    class Meta:
        model = Post
        fields = ["url", "title", "body"]
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
            "url": forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["url"].widget.attrs.update(
            {
                "hx-trigger": "change, keyup delay:250ms changed",
                "hx-get": reverse("metadata:scrape"),
                "hx-target": "#url-preview-wrapper",
                "hx-include": "#id_body,#id_title",  # TODO: remove ?
            }
        )
