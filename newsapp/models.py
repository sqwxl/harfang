from datetime import date, timedelta

from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm
from django.utils import timezone


class NewsSite(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200)
    rss_url = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    def __str__(self):
        return self.name


def validate_not_future(date_value):
    if date_value > date.today():
        raise ValidationError("Date cannot be in the future")


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=200, default="Anonymous")
    pub_date = models.DateTimeField("date published", validators=[validate_not_future])
    image_url = models.CharField(max_length=400, blank=True, null=True)
    image_caption = models.CharField(max_length=200, blank=True, null=True)

    news_site = models.ForeignKey("NewsSite", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_on"]


class SubmissionQuerySet(models.QuerySet):
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


class Submission(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True, related_name="edited_submissions"
    )
    deleted_on = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True, related_name="deleted_submissions"
    )
    flagged = models.BooleanField(default=False)
    flagged_by = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True, related_name="flagged_submissions"
    )

    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="submissions")

    comments = GenericRelation("treecomments.TreeComment", object_id_field="object_pk", related_query_name="submission")

    objects = SubmissionQuerySet.as_manager()

    def __str__(self):
        return self.title

    def clean(self):
        if not self.url and not self.text:
            raise ValidationError("A submission must have either a url or text")

    @property
    def score(self):
        return self.upvotes.count() - self.downvotes.count()  # type: ignore


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ["title", "url", "text"]


class SubmissionUpvote(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="submission_upvotes")
    submission = models.ForeignKey(
        "Submission", on_delete=models.CASCADE, null=True, blank=True, related_name="upvotes"
    )


class SubmissionDownvote(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="submission_downvotes")
    submission = models.ForeignKey(
        "Submission", on_delete=models.CASCADE, null=True, blank=True, related_name="downvotes"
    )
