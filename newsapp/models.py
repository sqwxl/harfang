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
    author = models.CharField(max_length=200, default="Unknown")
    source_url = models.CharField(max_length=200)
    date = models.DateTimeField("date published", validators=[validate_not_future])
    text = models.TextField()
    short = models.TextField()
    news_site = models.ForeignKey("NewsSite", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


def make_fake_news_sites(count):
    from faker import Faker

    fake = Faker()
    created = []
    for _ in range(count):
        created.append(
            NewsSite.objects.create(
                name=fake.company(),
                url=fake.url(),
                rss_url=fake.url(),
            )
        )
    return created
