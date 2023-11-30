from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.utils.translation import gettext as _

from app.utils.decorators import can_delete, can_edit, can_restore
from app.comments.models import Comment


def _user_can_x(predicate, forbidden_message):
    def decorator(fn):
        def wrapper(request, *args, **kwargs):
            comment = get_object_or_404(Comment, pk=kwargs["pk"])
            if predicate(request.user, comment):
                return fn(request, *args, **kwargs)
            else:
                # TODO: Flash
                return HttpResponseForbidden(forbidden_message)

        return wrapper

    return decorator


can_edit_comment = _user_can_x(
    can_edit,
    _("You are not allowed to edit this comment."),
)

can_delete_comment = _user_can_x(
    can_delete, _("You are not allowed to delete this comment.")
)

can_restore_comment = _user_can_x(
    can_restore, _("You are not allowed to restore this comment.")
)
