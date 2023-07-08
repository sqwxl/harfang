import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from newsapp.models import NewsItem, NewsSite

from ._factories import CommentFactory, NewsItemFactory, NewsSiteFactory, UserFactory

NUM_USERS = 20
NUM_SITES = 20
NUM_ITEMS = 40
NUM_COMMENTS_PER_ITEM = 10


class Command(BaseCommand):
    help = "Populate the database with test data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting existing data")
        # Delete all users except the superuser
        User.objects.all().exclude(is_superuser=True).delete()
        models = [NewsItem, NewsSite]
        for model in models:
            model.objects.all().delete()

        self.stdout.write("Creating new data")

        users = []
        for _ in range(NUM_USERS):
            users.append(UserFactory())

        news_sites = []
        for _ in range(NUM_SITES):
            news_sites.append(NewsSiteFactory())

        news_items = []
        for _ in range(NUM_ITEMS):
            news_items.append(NewsItemFactory(news_site=random.choice(news_sites)))

        for news_item in news_items:
            comments = []
            for _ in range(random.randint(0, NUM_COMMENTS_PER_ITEM)):
                comments.append(
                    CommentFactory(
                        news_item=news_item,
                        user=random.choice(users),
                        parent=random.choice([None, *comments]) if comments else None,
                    )
                )
