import factory
from django.contrib.auth.models import User
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
    pub_date = factory.Faker("date")
    content = factory.Faker("text")
    image_url = f"https://picsum.photos/{factory.Faker('random_int', min=200, max=400)}/{factory.Faker('random_int', min=200, max=400)}"
    image_caption = factory.Faker("sentence")
    url = factory.Faker("url")
    news_site = factory.SubFactory(NewsSiteFactory)
