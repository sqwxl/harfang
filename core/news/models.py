from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


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

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:article", kwargs={"pk": self.pk})
