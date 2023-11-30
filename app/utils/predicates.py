def can_edit(user, item):
    return user == item.user or user.is_moderator or user.is_staff


def can_delete(user, item):
    return user == item.user or user.is_moderator or user.is_staff


def can_restore(user, _):
    return user.is_moderator or user.is_staff
