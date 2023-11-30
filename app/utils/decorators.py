from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.utils.translation import gettext as _

from .predicates import can_delete, can_edit, can_restore


class AccessDecorators:
    def __init__(self, model_class):
        self.model_class = model_class
        self.edit = self._decorate(
            can_edit, _("You are not allowed to edit this comment.")
        )
        self.delete = self._decorate(
            can_delete, _("You are not allowed to delete this comment.")
        )
        self.restore = self._decorate(
            can_restore, _("You are not allowed to restore this comment.")
        )

    def _decorate(self, predicate, forbidden_message):
        def decorator(fn):
            def wrapper(request, *args, **kwargs):
                obj = get_object_or_404(self.model_class, pk=kwargs["pk"])
                if predicate(request.user, obj):
                    return fn(request, *args, **kwargs)
                else:
                    # TODO: Flash
                    return HttpResponseForbidden(forbidden_message)

            return wrapper

        return decorator
