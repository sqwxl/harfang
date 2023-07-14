import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from newsapp.models import Article, Comment, NewsSite, Post, Vote

from ._factories import (
    ArticleCommentFactory,
    ArticleFactory,
    ArticleVoteFactory,
    NewsSiteFactory,
    PostCommentFactory,
    PostFactory,
    PostVoteFactory,
    UserFactory,
)

NUM_SITES = 20
NUM_ARTICLES = 40
NUM_USERS = 40
NUM_POSTS = 40
NUM_COMMENTS_PER_ITEM = 20
NUM_VOTES_PER_ITEM = 20


class Command(BaseCommand):
    help = "Populate the database with test data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting existing data")
        # Delete all users except the superuser
        User.objects.all().exclude(is_superuser=True).delete()
        models = [Article, Post, NewsSite, Comment, Vote]
        for model in models:
            model.objects.all().delete()

        self.stdout.write("Creating new data")

        users = []
        for _ in range(NUM_USERS):
            users.append(UserFactory())

        news_sites = []
        for _ in range(NUM_SITES):
            news_sites.append(NewsSiteFactory())

        articles = []
        for _ in range(NUM_ARTICLES):
            articles.append(ArticleFactory(news_site=random.choice(news_sites)))

        for article in articles:
            comments = []
            for _ in range(random.randint(0, NUM_COMMENTS_PER_ITEM)):
                comments.append(
                    ArticleCommentFactory(
                        content_object=article,
                        user=random.choice(users),
                        parent=random.choice([None, *comments]) if comments else None,
                    )
                )
            for _ in range(random.randint(0, NUM_VOTES_PER_ITEM)):
                ArticleVoteFactory(
                    content_object=article,
                    user=random.choice(users),
                )

        posts = []
        for _ in range(NUM_POSTS):
            posts.append(PostFactory(user=random.choice(users)))

        for post in posts:
            comments = []
            for _ in range(random.randint(0, NUM_COMMENTS_PER_ITEM)):
                comments.append(
                    PostCommentFactory(
                        content_object=post,
                        user=random.choice(users),
                        parent=random.choice([None, *comments]) if comments else None,
                    )
                )
            for _ in range(random.randint(0, NUM_VOTES_PER_ITEM)):
                PostVoteFactory(
                    content_object=post,
                    user=random.choice(users),
                )
