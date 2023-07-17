from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


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
    comments = models.ForeignKey("ArticleComment", on_delete=models.CASCADE, null=True, related_name="article")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_on"]


class SubmissionQuerySet(models.QuerySet):
    def annotate_user_votes(self, user):
        return self.annotate(
            user_has_upvoted=models.Exists(
                SubmissionUpvote.objects.filter(user=user, submission=models.OuterRef("pk"))
            ),
            user_has_downvoted=models.Exists(
                SubmissionDownvote.objects.filter(user=user, submission=models.OuterRef("pk"))
            ),
        )

    def only_healthy(self):
        return self.exclude(is_healthy=False)

    def top_daily(self):
        return self.filter(created_on__gte=timezone.now() - timedelta(days=1)).order_by("-score")

    def top_weekly(self):
        return self.filter(created_on__gte=timezone.now() - timedelta(days=7)).order_by("-score")

    def top_monthly(self):
        return self.filter(created_on__gte=timezone.now() - timedelta(days=30)).order_by("-score")

    def top_yearly(self):
        return self.filter(created_on__gte=timezone.now() - timedelta(days=365)).order_by("-score")

    def top_all_time(self):
        return self.order_by("-score")

    def new(self):
        return self.order_by("-created_on")


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
    comments = models.ForeignKey("SubmissionComment", on_delete=models.CASCADE, null=True, related_name="submission")

    objects = SubmissionQuerySet.as_manager()

    def __str__(self):
        return self.title

    def clean(self):
        if not self.url and not self.text:
            raise ValidationError("A submission must have either a url or text")

    @property
    def score(self):
        return self.upvotes.count() - self.downvotes.count()  # type: ignore

    @property
    def comment_count(self):
        return self.comments.count()  # type: ignore

    @property
    def is_healthy(self):
        return not self.flagged and not self.deleted_on


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


class Comment(MPTTModel):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    flagged = models.BooleanField(default=False)
    created_on = models.DateTimeField("date published", auto_now_add=True)
    edited_on = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True, related_name="edited_comments"
    )
    deleted_on = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True, related_name="deleted_comments"
    )

    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")

    def __str__(self):
        return self.text[:20]

    @property
    def is_deleted(self):
        return self.deleted_on is not None

    @property
    def is_edited(self):
        return self.edited_on is not None

    @property
    def is_editable(self):
        return not self.is_deleted

    class MPTTMeta:
        order_insertion_by = ["-votes", "created_on"]

    class Meta:
        abstract = True


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": ""}


class SubmissionComment(Comment):
    submission = models.ForeignKey("Submission", on_delete=models.CASCADE, related_name="comments")


class ArticleComment(Comment):
    article = models.ForeignKey("Article", on_delete=models.CASCADE, related_name="comments")

    def reply(self, user, form):
        if form.is_valid():
            comment = ArticleComment.objects.create(
                user=user, article=self.article, parent=self, text=form.cleaned_data["text"]
            )
            return comment
