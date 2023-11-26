from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .common.mixins import PointsMixin


class User(PointsMixin, AbstractUser):
    def __str__(self):
        return self.username


class Profile(models.Model):
    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.CharField(_("bio"), blank=True, max_length=4)

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class PostQuerySet(models.QuerySet):
    def with_user_vote_status(self, user):
        return self.annotate(
            has_voted=models.Exists(
                PostVote.objects.filter(user=user, post=models.OuterRef("pk"))
            )
        )

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

    def latest(self):
        return self.order_by("-submit_date")

    def top(self):
        return self.order_by("-points")


class Post(PointsMixin, models.Model):
    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
    )
    title = models.CharField(_("title"), max_length=250)
    url = models.CharField(_("url"), max_length=200, blank=True)
    body = models.TextField(_("body"), blank=True)
    submit_date = models.DateTimeField(default=timezone.now, editable=False)
    # TODO enable_comments = models.BooleanField(default=True)

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._state.adding:
            self.user.increment_points()

    def delete(self, *args, **kwargs):
        self.user.decrement_points()
        super().delete(*args, **kwargs)

    def clean(self):
        if not self.url and not self.body:
            raise ValidationError("A submission must have either a url or text")

        super().clean()

    def get_absolute_url(self):
        return reverse("post", args=[str(self.pk)])

    def get_vote_url(self):
        return reverse("post_vote", args=[str(self.pk)])


class Vote(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submit_date = models.DateTimeField(default=timezone.now, editable=False)


class PostVote(Vote):
    class Meta:
        unique_together = ("user", "post")

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="votes"
    )

    def __str__(self):
        return f"{self.user} voted on {self.post}"

    def save(self, *args, **kwargs):
        if self.post.user == self.user:
            raise ValidationError("You cannot vote on your own submission")

        is_new = self._state.adding
        if is_new:
            self.post.increment_points()
            self.post.user.increment_points()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.post.decrement_points()
        self.post.user.decrement_points()
        super().delete(*args, **kwargs)


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
