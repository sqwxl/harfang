from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django_comments.forms import CommentForm
from mptt.fields import TreeNodeChoiceField

from .models import TreeComment


class TreeCommentForm(CommentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove unwanted fields
        for field_name in ["name", "email", "url"]:
            if field_name in self.fields:
                del self.fields[field_name]

    parent = TreeNodeChoiceField(queryset=TreeComment.objects.all(), widget=forms.HiddenInput, required=False)

    comment = forms.CharField(max_length=3000, widget=forms.Textarea)

    def get_comment_create_data(self, **kwargs):
        return dict(
            content_type=ContentType.objects.get_for_model(self.target_object),
            object_pk=str(self.target_object._get_pk_val()),
            parent=self.cleaned_data.get("parent"),
            comment=self.cleaned_data["comment"],
            submit_date=timezone.now(),
            site_id=settings.SITE_ID,
        )

    def check_for_duplicate_comment(self, new):
        possible_duplicates = TreeComment.objects.filter(
            content_type=new.content_type,
            object_pk=new.object_pk,
            parent=new.parent,
            user=new.user,
        )
        for old in possible_duplicates:
            if old.submit_date.date() == new.submit_date.date() and old.comment == new.comment:
                return old

        return new
