from datetime import date

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


class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    author = models.CharField(max_length=200, default="Anonymous")
    pub_date = models.DateTimeField("date published", validators=[validate_not_future])
    text = models.TextField()
    image_url = models.CharField(max_length=400, blank=True)
    image_caption = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200)
    news_site = models.ForeignKey("NewsSite", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    news_item = models.ForeignKey("NewsItem", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    text = models.TextField()
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")

    def __str__(self):
        return self.text[:20]

    class MPTTMeta:
        order_insertion_by = ["-votes", "pub_date"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": ""}
