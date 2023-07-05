import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from newsapp.models import NewsItem, NewsSite

from ._factories import NewsItemFactory, NewsSiteFactory, UserFactory

NUM_USERS = 10
NUM_SITES = 60
NUM_ITEMS = 1000


class Command(BaseCommand):
    help = "Populate the database with test data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting existing data")
        models = [NewsItem, NewsSite, User]
        for model in models:
            model.objects.all().delete()

        self.stdout.write("Creating new data")
        for _ in range(NUM_USERS):
            UserFactory()

        news_sites = []
        for _ in range(NUM_SITES):
            news_sites.append(NewsSiteFactory())

        for _ in range(NUM_ITEMS):
            NewsItemFactory(news_site=random.choice(news_sites))
