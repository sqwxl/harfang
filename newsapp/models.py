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
    content = models.TextField()
    image_url = models.CharField(max_length=400, blank=True)
    image_caption = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200)
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


def make_fake_news_items(count):
    from faker import Faker

    fake = Faker()
    created = []
    for _ in range(count):
        created.append(
            NewsItem.objects.create(
                title=fake.sentence(),
                subtitle=fake.sentence(),
                author=fake.name(),
                pub_date=fake.date_time_this_year(),
                content=fake.text(),
                image=fake.image_url(),
                image_caption=fake.sentence(),
                url=fake.url(),
                news_site=NewsSite.objects.order_by("?").first(),
            )
        )
    return created
