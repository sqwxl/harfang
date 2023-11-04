from django_comments.forms import CommentForm as BaseCommentForm

from . import get_model


class CommentForm(BaseCommentForm):
    def get_comment_model(self):
        return get_model()
