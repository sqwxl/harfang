from django.db import models
from django.urls import reverse
from django_comments.abstracts import CommentAbstractModel
from django_comments.managers import CommentManager
from mptt.models import MPTTModel, TreeForeignKey, TreeManager


class TreeCommentManager(TreeManager, CommentManager):
    pass


class TreeComment(MPTTModel, CommentAbstractModel):
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    objects = TreeCommentManager()

    class Meta(CommentAbstractModel.Meta):
        verbose_name = "comment"
        verbose_name_plural = "comments"

    class MPTTMeta:
        order_insertion_by = ["submit_date"]

    def get_absolute_url(self):
        return reverse("comment", kwargs={"pk": self.pk})
