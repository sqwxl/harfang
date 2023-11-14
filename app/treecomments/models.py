from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_comments.abstracts import BaseCommentAbstractModel
from django_comments.managers import CommentManager
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

from app.common.mixins import PointsMixin


class TreeCommentManager(TreeManager, CommentManager):
    pass


class TreeComment(PointsMixin, MPTTModel, BaseCommentAbstractModel):
    class MPTTMeta:
        order_insertion_by = ["submit_date"]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="user", null=True, on_delete=models.SET_NULL, related_name="comments"
    )
    submit_date = models.DateTimeField(default=timezone.now, editable=False)
    comment = models.TextField(max_length=3000)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    is_removed = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Check this box if the comment is inappropriate. "
        'A "This comment has been removed" message will '
        "be displayed instead.",
    )

    objects = TreeCommentManager()

    def get_absolute_url(self):
        return reverse("comment", kwargs={"pk": self.pk})

    def get_content_object_url(self):
        return self.content_object.get_absolute_url()  # type: ignore
