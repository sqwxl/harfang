from django import forms
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from app.forms import AppModelForm
from app.markdown.widgets import MarkdownTextarea

from .models import Post


class PostForm(AppModelForm):
    class Meta:
        model = Post
        fields = ["url", "title", "body", "image_url", "image_alt"]
        labels = {
            "url": _("URL"),
        }
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
            "image_url": forms.HiddenInput(),
            "image_alt": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["url"].widget.attrs.update(
            {
                "hx-trigger": "change, keyup delay:400ms changed",
                "hx-get": reverse("metadata:scrape"),
                "hx-target": "#url-preview-wrapper",
                "hx-indicator": "#url-preview-wrapper",
            }
        )
        self.fields["body"].widget = MarkdownTextarea(
            attrs={"rows": 4}, html=getattr(self.instance, "body_html", "")
        )
