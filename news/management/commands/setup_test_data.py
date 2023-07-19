import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from news.models import Article, NewsSite, Submission, SubmissionDownvote, SubmissionUpvote
from treecomments.models import TreeComment

from ._factories import (
    ArticleCommentFactory,
    ArticleFactory,
    NewsSiteFactory,
    SubmissionCommentFactory,
    SubmissionDownvoteFactory,
    SubmissionFactory,
    SubmissionUpvoteFactory,
    UserFactory,
)

NUM_USERS = 40
NUM_SITES = 20
NUM_ARTICLES = 40
NUM_SUBMISSIONS = 60
NUM_COMMENTS_PER_SUBMISSION = 20
NUM_VOTES_PER_SUBMISSION = 30


class Command(BaseCommand):
    help = "Populate the database with test data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting existing data")
        # Delete all users except the superuser
        User.objects.all().exclude(is_superuser=True).delete()
        models = [Article, Submission, NewsSite, TreeComment, SubmissionUpvote, SubmissionDownvote]
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
            for _ in range(random.randint(0, NUM_COMMENTS_PER_SUBMISSION)):
                comments.append(
                    ArticleCommentFactory(
                        content_object=article,
                        user=random.choice(users),
                        parent=random.choice([None, *comments]) if comments else None,
                    )
                )

        submissions = []
        for _ in range(NUM_SUBMISSIONS):
            submissions.append(SubmissionFactory(user=random.choice(users)))

        for submission in submissions:
            comments = []
            for _ in range(random.randint(0, NUM_COMMENTS_PER_SUBMISSION)):
                comments.append(
                    SubmissionCommentFactory(
                        content_object=submission,
                        user=random.choice(users),
                        parent=random.choice([None, *comments]) if comments else None,
                    )
                )
            users_drain = iter(users.copy())
            for _ in range(random.randint(0, NUM_VOTES_PER_SUBMISSION)):
                is_up = random.choice([True, False])
                user = next(users_drain)
                if is_up:
                    SubmissionUpvoteFactory(
                        submission=submission,
                        user=user,
                    )
                else:
                    SubmissionDownvoteFactory(
                        submission=submission,
                        user=user,
                    )
