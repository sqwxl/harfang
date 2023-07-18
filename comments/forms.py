from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str
from django.utils.text import get_text_list
from django.utils.translation import gettext, ngettext
from django_comments.forms import COMMENT_MAX_LENGTH, CommentSecurityForm

from .models import TreeComment

# based off of django_comments.forms


class CommentForm(CommentSecurityForm):
    text = forms.CharField(label="", widget=forms.Textarea, max_length=COMMENT_MAX_LENGTH)
    honeypot = forms.CharField(
        required=False, label="If you enter anythiong in this field " "your comment will be treated as spam"
    )

    def get_comment_object(self, site_id=None):
        """
        Return a new (unsaved) comment object based on the information in this
        form. Assumes that the form is already validated and will throw a
        ValueError if not.

        Does not set any of the fields that would come from a Request object
        (i.e. ``user`` or ``ip_address``).
        """
        if not self.is_valid():
            raise ValueError("get_comment_object may only be called on valid forms")

        CommentModel = self.get_comment_model()
        new = CommentModel(**self.get_comment_create_data(site_id=site_id))
        new = self.check_for_duplicate_comment(new)

        return new

    def get_comment_model(self):
        """
        Get the comment model to create with this form. Subclasses in custom
        comment apps should override this, get_comment_create_data, and perhaps
        check_for_duplicate_comment to provide custom comment models.
        """
        return TreeComment

    def get_comment_create_data(self, site_id=None):
        """
        Returns the dict of data to be used to create a comment. Subclasses in
        custom comment apps that override get_comment_model can override this
        method to add extra fields onto a custom comment model.
        """
        return dict(
            content_type=ContentType.objects.get_for_model(self.target_object),
            object_pk=force_str(self.target_object._get_pk_val()),
            text=self.cleaned_data["text"],
            site_id=site_id or getattr(settings, "SITE_ID", None),
        )

    def check_for_duplicate_comment(self, new):
        """
        Check that a submitted comment isn't a duplicate. This might be caused
        by someone posting a comment twice. If it is a dup, silently return the *previous* comment.
        """
        possible_duplicates = (
            self.get_comment_model()
            ._default_manager.using(self.target_object._state.db)
            .filter(
                content_type=new.content_type,
                object_pk=new.object_pk,
                user=new.user,
            )
        )
        for old in possible_duplicates:
            if old.created_on.date() == new.created_on.date() and old.text == new.text:
                return old

        return new

    def clean_comment(self):
        """
        If COMMENTS_ALLOW_PROFANITIES is False, check that the comment doesn't
        contain anything in PROFANITIES_LIST.
        """
        comment = self.cleaned_data["comment"]
        if not getattr(settings, "COMMENTS_ALLOW_PROFANITIES", False) and getattr(settings, "PROFANITIES_LIST", False):
            bad_words = [w for w in settings.PROFANITIES_LIST if w in comment.lower()]
            if bad_words:
                raise forms.ValidationError(
                    ngettext(
                        "Watch your mouth! The word %s is not allowed here.",
                        "Watch your mouth! The words %s are not allowed here.",
                        len(bad_words),
                    )
                    % get_text_list([f"\"{i[0]}{'-' * (len(i) - 2)}{i[-1]}\"" for i in bad_words], gettext("and"))
                )
        return comment
