import random

from django.core.management.base import BaseCommand
from django.db import transaction

from app.comments.models import Comment, CommentVote
from app.posts.models import Post, PostVote
from app.users.models import User


from ._factories import (
    CommentFactory,
    CommentVoteFactory,
    PostFactory,
    PostVoteFactory,
    UserFactory,
)

NUM_USERS = 200
NUM_POSTS = 60
NUM_COMMENTS_PER_POST = 20
NUM_VOTES_PER_POST = 30
NUM_VOTES_PER_COMMENT = 10


class Command(BaseCommand):
    help = "Populate the database with test data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting existing data")
        # Delete all users except the superuser
        User.objects.all().exclude(is_superuser=True).delete()
        # Delete all model instances
        models = [Post, Comment, PostVote, CommentVote]
        for model in models:
            model.objects.all().delete()

        self.stdout.write("Creating new data")

        users = []
        for i in range(NUM_USERS):
            users.append(UserFactory(username=f"user{i}"))

        # create superuser
        users.append(
            UserFactory(is_superuser=True, is_staff=True, username="admin")
        )

        posts = []
        for _ in range(NUM_POSTS):
            posts.append(PostFactory(user=random.choice(users)))

        for post in posts:
            comments = []
            for _ in range(random.randint(0, NUM_COMMENTS_PER_POST)):
                parent = random.choice([None, *comments])
                comment = CommentFactory(
                    user=random.choice(users), post=post, parent=parent
                )
                # if parent:
                #     parent.refresh_from_db()
                comments.append(comment)
            users_drain = iter(users.copy())
            for _ in range(random.randint(0, NUM_VOTES_PER_POST)):
                user = next(users_drain)
                if user != post.user and random.choice([True, False]):
                    PostVoteFactory(
                        post=post,
                        user=user,
                    )

        comments = Comment.objects.all()

        for comment in comments:
            users_drain = iter(users.copy())
            for _ in range(random.randint(0, NUM_VOTES_PER_COMMENT)):
                user = next(users_drain)
                if user != comment.user and random.choice([True, False]):
                    CommentVoteFactory(
                        comment=comment,
                        user=user,
                    )
