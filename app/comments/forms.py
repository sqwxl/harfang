from django import forms
from django.conf import settings
from django.utils.text import get_text_list
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from mptt.fields import TreeNodeChoiceField

from app.forms import AppModelForm

from .models import Comment


class CommentForm(AppModelForm):
    class Meta:
        model = Comment
        fields = ["body", "post", "parent", "honeypot"]

    def __init__(self, *args, **kwargs):
        # use parent's post if parent is set in initial dict
        if initial := kwargs.get("initial"):
            if "parent" in initial:
                initial["post"] = initial["parent"].post

        super().__init__(*args, **kwargs)
        self.fields["post"].widget = forms.HiddenInput()

    parent = TreeNodeChoiceField(
        queryset=Comment.objects.all(), widget=forms.HiddenInput, required=False
    )

    body = forms.CharField(
        label="",
        widget=forms.Textarea,
        help_text=_("Maximum {n} characters").format(
            n=settings.COMMENT_BODY_MAX_LENGTH
        ),
    )

    honeypot = forms.CharField(
        required=False,
        label=_(
            "If you enter anything in this field "
            "your comment will be treated as spam"
        ),
    )

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value

    def check_for_duplicate_comment(self, new):
        possible_duplicates = Comment.objects.filter(
            user=new.user,
            post=new.post,
            parent=new.parent,
        )
        for old in possible_duplicates:
            if (
                old.submit_date.date() == new.submit_date.date()
                and old.body == new.body
            ):
                return old

        return

    def clean_body(self):
        """
        If COMMENTS_BLOCK_PROFANITIES is True, check that the comment doesn't
        contain anything in PROFANITIES_LIST.
        """
        body = self.cleaned_data["body"]
        if getattr(settings, "COMMENTS_BLOCK_PROFANITIES", True) and getattr(
            settings, "PROFANITIES_LIST", False
        ):
            bad_words = [
                w for w in settings.PROFANITIES_LIST if w in body.lower()
            ]
            if bad_words:
                raise forms.ValidationError(
                    ngettext(
                        "Watch your mouth! The word %s is not allowed here.",
                        "Watch your mouth! The words %s are not allowed here.",
                        len(bad_words),
                    )
                    % get_text_list(
                        [
                            f"\"{i[0]}{'*' * (len(i) - 2)}{i[-1]}\""
                            for i in bad_words
                        ],
                        gettext("and"),
                    )
                )
        return body
