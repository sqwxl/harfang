from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django.utils import timezone


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="submissions")
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    submit_date = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=200)
    enable_comments = models.BooleanField(default=True)

    comments = GenericRelation("comments.models.Comment", object_id_field="object_pk", related_query_name="post")

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title

    def clean(self):
        if not self.url and not self.body:
            raise ValidationError("A submission must have either a url or text")

    @property
    def score(self):
        return self.upvotes.count() - self.downvotes.count()  # type: ignore

    def get_absolute_url(self):
        return reverse("posts_detail", kwargs={"pk": self.pk})


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "url", "text"]
