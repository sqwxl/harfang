from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from mptt.querysets import TreeQuerySet

from app.common.mixins import PointsMixin
from app.models import CommentVote


class CommentQuerySet(TreeQuerySet):
    def with_user_vote_status(self, user):
        return self.annotate(
            has_voted=models.Exists(CommentVote.objects.filter(user=user, comment=models.OuterRef("pk")))
        )

    def ordered_by_points(self):
        return self.order_by("-points", "submit_date")


class CommentManager(TreeManager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)


class Comment(PointsMixin, MPTTModel):
    class MPTTMeta:
        order_insertion_by = ["submit_date"]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="user", null=True, on_delete=models.SET_NULL, related_name="comments"
    )
    post = models.ForeignKey("app.Post", on_delete=models.CASCADE, related_name="comments")
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    body = models.TextField(max_length=3000)

    submit_date = models.DateTimeField(default=timezone.now, editable=False)

    is_removed = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Check this box if the comment is inappropriate. "
        'A "This comment has been removed" message will '
        "be displayed instead.",
    )

    objects = CommentManager()

    def get_absolute_url(self):
        return reverse("comment", kwargs={"pk": self.pk})
