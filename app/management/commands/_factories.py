from datetime import datetime

import factory
import faker
from django.db.models.signals import post_save
from django.utils import timezone

from app.comments.models import Comment, CommentVote
from app.posts.models import Post, PostVote
from app.users.models import Profile, User


fake = faker.Faker()


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    bio = factory.Faker("paragraph", nb_sentences=3, variable_nb_sentences=True)
    # We pass in profile=None to prevent UserFactory from creating another profile
    # (this disables the RelatedFactory)
    # https://factoryboy.readthedocs.io/en/stable/recipes.html#example-django-s-profile
    user = factory.SubFactory("app._factories.UserFactory", profile=None)


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = factory.django.Password("password")
    email = factory.Faker("email")
    date_joined = factory.Faker(
        "date_time_between",
        start_date=datetime(2023, 8, 1),
        tzinfo=timezone.get_current_timezone(),
    )
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = factory.Faker("boolean", chance_of_getting_true=1)
    is_active = factory.Faker("boolean", chance_of_getting_true=95)

    # We pass in 'user' to link the generated Profile to our just-generated User
    # This will call ProfileFactory(user=our_new_user), thus skipping the SubFactory.
    profile = factory.RelatedFactory(
        ProfileFactory, factory_related_name="user"
    )


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence")
    body = factory.Faker(
        "paragraph", nb_sentences=10, variable_nb_sentences=True
    )
    url = factory.Faker("url")
    submit_date = factory.Faker(
        "date_time_between",
        start_date=factory.SelfAttribute("..user.date_joined"),
        tzinfo=timezone.get_current_timezone(),
    )
    # enable_comments = factory.Faker("boolean", chance_of_getting_true=95)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)

    post = factory.SubFactory(PostFactory)
    parent = factory.SubFactory("app._factories.CommentFactory")

    body = factory.Faker(
        "paragraph", nb_sentences=10, variable_nb_sentences=True
    )

    @factory.lazy_attribute
    def submit_date(self):
        start_date = (
            self.post.submit_date
            if not self.parent
            else self.parent.submit_date
        )
        if start_date < self.user.date_joined:
            start_date = self.user.date_joined

        return fake.date_time_between(
            start_date=start_date,
            tzinfo=timezone.get_current_timezone(),
        )


class PostVoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostVote

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)

    @factory.lazy_attribute
    def submit_date(self):
        start_date = self.post.submit_date
        if start_date < self.user.date_joined:
            start_date = self.user.date_joined

        return fake.date_time_between(
            start_date=start_date,
            tzinfo=timezone.get_current_timezone(),
        )


class CommentVoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommentVote

    user = factory.SubFactory(UserFactory)
    comment = factory.SubFactory(CommentFactory)

    @factory.lazy_attribute
    def submit_date(self):
        start_date = self.comment.submit_date
        if start_date < self.user.date_joined:
            start_date = self.user.date_joined

        return fake.date_time_between(
            start_date=start_date,
            tzinfo=timezone.get_current_timezone(),
        )
