def get_model():
    from .models import Comment

    return Comment


def get_form():
    from .forms import CommentForm

    return CommentForm
