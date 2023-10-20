from django.db import models
from django_comments.abstracts import COMMENT_MAX_LENGTH, BaseCommentAbstractModel
from mptt.models import MPTTModel, TreeForeignKey

from .managers import CommentManager


class Comment(MPTTModel, BaseCommentAbstractModel):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="%(class)s_comments")
    text = models.TextField(max_length=COMMENT_MAX_LENGTH)
    created_on = models.DateTimeField(auto_now_add=True)

    is_flagged = models.BooleanField(default=False)
    edited_on = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_edited_comments",
    )
    deleted_on = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_deleted_comments",
    )

    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")

    objects = CommentManager()

    class Meta:
        ordering = ("created_on",)

    class MPTTMeta:
        order_insertion_by = ["created_on"]

    def __str__(self):
        return f"{self.user.username}: {self.text[:50]}..."

    @property
    def is_deleted(self):
        return self.deleted_on is not None

    @property
    def is_edited(self):
        return self.edited_on is not None

    @property
    def is_editable(self):
        return not self.is_deleted
