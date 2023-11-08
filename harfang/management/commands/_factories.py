import factory
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from app.models import Post, User
from app.treecomments.models import TreeComment


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = factory.Faker("password")
    email = factory.Faker("email")
    date_joined = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = factory.Faker("boolean", chance_of_getting_true=1)
    is_active = factory.Faker("boolean", chance_of_getting_true=95)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence")
    body = factory.Faker("paragraph", nb_sentences=10, variable_nb_sentences=True)
    url = factory.Faker("url")
    submit_date = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    enable_comments = factory.Faker("boolean", chance_of_getting_true=95)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TreeComment

    user = factory.SubFactory(UserFactory)
    comment = factory.Faker("paragraph", nb_sentences=10, variable_nb_sentences=True)
    submit_date = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())

    content_type = ContentType.objects.get_for_model(Post)
    object_pk = factory.SelfAttribute("content_object.id")
    content_object = factory.SubFactory(PostFactory)

    parent = factory.SubFactory("harfang._factories.CommentFactory")
