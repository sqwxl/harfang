from django import template

register = template.Library()


@register.filter(name="can_moderate")
def can_moderate(user, comment):
    return user == comment.user or user.has_perm("comments.can_moderate")
