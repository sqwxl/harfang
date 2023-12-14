from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import DEFERRED
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app.common.mixins import PointsMixin
from app.markdown.utils import md_to_html
from app.models import Vote


class PostQuerySet(models.QuerySet):
    def day(self):
        return self.filter(submit_date__gte=timezone.now() - timedelta(days=1))

    def week(self):
        return self.filter(submit_date__gte=timezone.now() - timedelta(days=7))

    def month(self):
        return self.filter(submit_date__gte=timezone.now() - timedelta(days=30))

    def year(self):
        return self.filter(
            submit_date__gte=timezone.now() - timedelta(days=365)
        )

    def top(self):
        return self.order_by("-points")


class Post(PointsMixin, models.Model):
    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        get_latest_by = "submit_date"
        indexes = [models.Index(fields=["submit_date", "points"])]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
    )
    title = models.CharField(
        _("title"), max_length=settings.POST_TITLE_MAX_LENGTH
    )
    url = models.URLField(
        _("url"),
        blank=True,
        max_length=settings.POST_URL_MAX_LENGTH,
    )
    body = models.CharField(
        _("body"), blank=True, max_length=settings.POST_BODY_MAX_LENGTH
    )
    body_html = models.TextField(_("html"), blank=True, null=True)
    image_url = models.URLField(
        _("image"),
        blank=True,
        null=True,
        max_length=settings.POST_URL_MAX_LENGTH,
    )
    image_alt = models.CharField(_("image alt"), blank=True, max_length=255)
    submit_date = models.DateTimeField(
        _("date submitted"), default=timezone.now, editable=False
    )
    # TODO enable_comments = models.BooleanField(default=True)

    objects = PostQuerySet.as_manager()

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(
            zip(
                field_names,
                (value for value in values if value is not DEFERRED),
            )
        )
        return instance

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.body_html = md_to_html(self.body)
        elif self.body != self._loaded_values["body"]:
            # updating an existing instance
            self.body_html = md_to_html(self.body)
        super().save(*args, **kwargs)

    def clean(self):
        if not self.url and not self.body:
            raise ValidationError("A submission must have either a url or text")

        super().clean()

    def get_absolute_url(self):
        return reverse("posts:detail", args=[str(self.pk)])

    def get_vote_url(self):
        return reverse("posts:vote", args=[str(self.pk)])


class PostVote(Vote):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_vote")
        ]

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="votes"
    )

    def __str__(self):
        return f"{self.user} voted on {self.post}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.post.increment_points()
            self.post.user.increment_points()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.post.decrement_points()
        self.post.user.decrement_points()
        super().delete(*args, **kwargs)


@receiver(post_save, sender=Post)
def create_post_vote_on_post_create(sender, instance, created, **kwargs):
    if created:
        PostVote.objects.create(user=instance.user, post=instance)


@receiver(post_delete, sender=Post)
def delete_post_vote_on_post_delete(sender, instance, **kwargs):
    # PostVote.objects.filter(user=instance.user, post=instance).delete()
    pass  # handled at db level (CASCADE)
