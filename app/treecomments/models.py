from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_comments.abstracts import CommentAbstractModel
from django_comments.managers import CommentManager
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

from app.common.mixins import PointsMixin


class TreeCommentManager(TreeManager, CommentManager):
    pass


class TreeComment(PointsMixin, MPTTModel, CommentAbstractModel):
    submit_date = models.DateTimeField(default=timezone.now, editable=False)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    objects = TreeCommentManager()

    class MPTTMeta:
        order_insertion_by = ["submit_date"]

    def get_absolute_url(self):
        return reverse("comment", kwargs={"pk": self.pk})
