from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django.utils import timezone

from app.treecomments.models import TreeComment


class User(AbstractUser):
    pass


def validate_not_future(date_value):
    if date_value > date.today():
        raise ValidationError("Date cannot be in the future")


class PostQuerySet(models.QuerySet):
    # def annotate_user_votes(self, user):
    #     return self.annotate(
    #         user_has_upvoted=models.Exists(
    #             SubmissionUpvote.objects.filter(user=user.id, submission=models.OuterRef("pk"))
    #         ),
    #         user_has_downvoted=models.Exists(
    #             SubmissionDownvote.objects.filter(user=user.id, submission=models.OuterRef("pk"))
    #         ),
    #     )

    def only_healthy(self):
        return self.filter(flagged=False, deleted_on__isnull=True)

    def daily(self):
        return self.filter(created_on__gte=timezone.now() - timedelta(days=1))

    def weekly(self):
        return self.filter(created_on__gte=timezone.now() - timedelta(days=7))

    def monthly(self):
        return self.filter(created_on__gte=timezone.now() - timedelta(days=30))

    def yearly(self):
        return self.filter(created_on__gte=timezone.now() - timedelta(days=365))


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="posts")
    title = models.CharField(max_length=250)
    url = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    submit_date = models.DateTimeField(auto_now_add=True)
    enable_comments = models.BooleanField(default=True)

    comments = GenericRelation(
        "treecomments.models.TreeComment", object_id_field="object_pk", related_query_name="target"
    )

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title

    def clean(self):
        if not self.url and not self.body:
            raise ValidationError("A submission must have either a url or text")

        super().clean()

    @property
    def score(self):
        return self.upvotes.count() - self.downvotes.count()  # type: ignore

    def get_absolute_url(self):
        return reverse("post", kwargs={"pk": self.pk})


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "url", "body"]


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submit_date = models.DateTimeField(auto_now_add=True)


class PostVote(Vote):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")


class CommentVote(Vote):
    comment = models.ForeignKey(TreeComment, on_delete=models.CASCADE, related_name="votes")
