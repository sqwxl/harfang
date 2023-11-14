def get_model():
    from app.treecomments.models import TreeComment

    return TreeComment


def get_form():
    from app.treecomments.forms import TreeCommentForm

    return TreeCommentForm
