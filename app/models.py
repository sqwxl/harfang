from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from .common.mixins import PointsMixin


class User(PointsMixin, AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class PostQuerySet(models.QuerySet):
    def with_user_vote_status(self, user):
        return self.annotate(has_voted=models.Exists(PostVote.objects.filter(user=user, post=models.OuterRef("pk"))))

    def day(self):
        return self.filter(submit_date__gte=timezone.now() - timedelta(days=1))

    def week(self):
        return self.filter(submit_date__gte=timezone.now() - timedelta(days=7))

    def month(self):
        return self.filter(submit_date__gte=timezone.now() - timedelta(days=30))

    def year(self):
        return self.filter(submit_date__gte=timezone.now() - timedelta(days=365))

    def latest(self):
        return self.order_by("-submit_date")

    def top(self):
        return self.order_by("-points")


class Post(PointsMixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="posts")
    title = models.CharField(max_length=250)
    url = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    submit_date = models.DateTimeField(default=timezone.now, editable=False)
    enable_comments = models.BooleanField(default=True)
    comments = GenericRelation("comments.Comment", object_id_field="object_pk")

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


class PostVote(models.Model):
    class Meta:
        unique_together = ("user", "post")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submit_date = models.DateTimeField(default=timezone.now, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")

    def save(self, *args, **kwargs):
        if self.post.user == self.user:
            raise ValidationError("You cannot vote on your own submission")

        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            self.post.increment_points()
            self.post.user.increment_points()

    def delete(self, *args, **kwargs):
        self.post.decrement_points()
        self.post.user.decrement_points()
        super().delete(*args, **kwargs)


class CommentVote(models.Model):
    class Meta:
        unique_together = ("user", "comment")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submit_date = models.DateTimeField(default=timezone.now, editable=False)
    comment = models.ForeignKey("comments.Comment", on_delete=models.CASCADE, related_name="votes")

    def save(self, *args, **kwargs):
        if self.comment.user == self.user:
            raise ValidationError("You cannot vote on your own comment")

        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            self.comment.increment_points()
            self.comment.user.increment_points()

    def delete(self, *args, **kwargs):
        self.comment.decrement_points()
        self.comment.user.decrement_points()
        super().delete(*args, **kwargs)
