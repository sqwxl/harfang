from datetime import date

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm
from mptt.models import MPTTModel, TreeForeignKey


class NewsSite(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    rss_url = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="logos/", blank=True)

    def __str__(self):
        return self.name


def validate_not_future(date_value):
    if date_value > date.today():
        raise ValidationError("Date cannot be in the future")


class Vote(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    value = models.BooleanField()  # True = upvote, False = downvote
    created_on = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"{self.user.username} voted {self.value}"


class FeedItem(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    url = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

    votes = GenericRelation("Vote")

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Article(FeedItem):
    subtitle = models.CharField(max_length=200, blank=True)
    author = models.CharField(max_length=200, default="Anonymous")
    pub_date = models.DateTimeField("date published", validators=[validate_not_future])
    image_url = models.CharField(max_length=400, blank=True)
    image_caption = models.CharField(max_length=200, blank=True)
    news_site = models.ForeignKey("NewsSite", on_delete=models.CASCADE)

    comments = GenericRelation("Comment")


class Post(FeedItem):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
    )
    edited_on = models.DateTimeField(null=True, blank=True)
    flagged = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)

    comments = GenericRelation("Comment")


class Comment(MPTTModel):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    votes = models.IntegerField(default=0)
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
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": ""}
