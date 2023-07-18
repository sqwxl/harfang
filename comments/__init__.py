def get_model():
    from comments.models import Comment

    return Comment


def get_form():
    from comments.forms import CommentForm

    return CommentForm
