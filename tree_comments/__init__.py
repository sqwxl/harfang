def get_model():
    from comments.models import TreeComment

    return TreeComment


def get_form():
    from comments.forms import CommentForm

    return CommentForm
