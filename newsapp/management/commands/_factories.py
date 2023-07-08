import random

import factory
from django.contrib.auth.models import User
from django.utils import timezone
from factory.django import DjangoModelFactory

from newsapp.models import NewsItem, NewsSite


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = factory.Faker("password")


class NewsSiteFactory(DjangoModelFactory):
    class Meta:
        model = NewsSite

    name = factory.Faker("company")
    url = factory.Faker("url")
    rss_url = factory.Faker("url")


class NewsItemFactory(DjangoModelFactory):
    class Meta:
        model = NewsItem

    title = factory.Faker("sentence")
    subtitle = factory.Faker("sentence")
    author = factory.Faker("name")
    pub_date = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    text = factory.Faker("paragraph", nb_sentences=10, variable_nb_sentences=True)
    image_url = factory.LazyFunction(
        lambda: f"https://picsum.photos/{random.randint(200, 400)}/{random.randint(200, 400)}"
    )
    image_caption = factory.Faker("sentence")
    url = factory.Faker("url")
    news_site = factory.SubFactory(NewsSiteFactory)
