from django import template

from app.utils.predicates import can_edit, can_delete, can_restore

register = template.Library()


@register.filter(name="can_edit")
def can_edit_comment(user, comment):
    return can_edit(user, comment)


@register.filter(name="can_delete")
def can_delete_comment(user, comment):
    return can_delete(user, comment)


@register.filter(name="can_restore")
def can_restore_comment(user, comment):
    return can_restore(user, comment)
