from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

from app.common.mixins import PointsMixin
from app.models import Vote


class CommentManager(TreeManager):
    def with_user_vote_status(self, user):
        return self.get_queryset().annotate(
            has_voted=models.Exists(
                CommentVote.objects.filter(
                    user=user, comment=models.OuterRef("pk")
                )
            )
        )


class Comment(MPTTModel, PointsMixin):
    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        indexes = [
            models.Index(fields=["submit_date"]),
        ]

    class MPTTMeta:
        order_insertion_by = ["submit_date"]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="comments",
    )

    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="comments"
    )

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    body = models.CharField(
        _("comment"), max_length=settings.COMMENT_BODY_MAX_LENGTH
    )

    submit_date = models.DateTimeField(default=timezone.now, editable=False)

    is_removed = models.BooleanField(_("is removed"), default=False)

    is_edited = models.BooleanField(_("was edited"), default=False)

    objects = CommentManager()

    def __str__(self):
        return f"{self.user}: {self.body[:40]}"

    def get_absolute_url(self):
        return reverse("comments:detail", kwargs={"pk": self.pk})

    def get_post_url(self):
        return self.post.get_absolute_url()

    def get_vote_url(self):
        return reverse("comments:vote", kwargs={"pk": self.pk})


class CommentVote(Vote):
    class Meta:
        unique_together = ("user", "comment")

    comment = models.ForeignKey(
        "comments.Comment", on_delete=models.CASCADE, related_name="votes"
    )

    def __str__(self):
        return f"{self.user} voted on {self.comment}"

    def save(self, *args, **kwargs):
        if self.comment.user == self.user:
            raise ValidationError("You cannot vote on your own comment")

        is_new = self._state.adding
        if is_new:
            self.comment.increment_points()
            self.comment.user.increment_points()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # if comment exists, decrement its points
        if self.comment:
            self.comment.decrement_points()
            self.comment.user.decrement_points()
        super().delete(*args, **kwargs)
