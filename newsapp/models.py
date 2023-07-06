from datetime import date

from django.core.exceptions import ValidationError
from django.db import models


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
    text_content = models.TextField()
    image_url = models.CharField(max_length=400, blank=True)
    image_caption = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200)
    news_site = models.ForeignKey("NewsSite", on_delete=models.CASCADE)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    news_item = models.ForeignKey("NewsItem", on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    text_content = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text_content
