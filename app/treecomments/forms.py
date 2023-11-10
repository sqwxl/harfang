from django.forms import HiddenInput
from django_comments.forms import CommentForm
from mptt.fields import TreeNodeChoiceField

from .models import TreeComment


class TreeCommentForm(CommentForm):
    parent = TreeNodeChoiceField(queryset=TreeComment.objects.all(), widget=HiddenInput)

    def get_comment_create_data(self, **kwargs):
        data = super().get_comment_create_data(**kwargs)
        data["parent"] = self.cleaned_data["parent"]
        return data
