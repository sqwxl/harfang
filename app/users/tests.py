from django.conf import settings
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from app.comments.models import Comment

from app.posts.models import Post
from .models import User


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name="Moderator")
        cls.user = User.objects.create(username="whatever")

    def test_auto_created_profile_exists(self):
        self.assertIsNotNone(self.user.profile)

    def test_user_is_not_moderator(self):
        self.assertFalse(self.user.is_moderator)

    def test_user_is_moderator(self):
        self.user.groups.add(self.group)
        self.assertTrue(self.user.is_moderator)


class CreateViewTest(TestCase):
    def test_create_view_get(self):
        res = self.client.get(reverse("users:create"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "base_form.html")

    def test_create_view_post(self):
        res = self.client.post(
            reverse("users:create"),
            data={
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("login"))

    def test_create_view_post_invalid(self):
        res = self.client.post(
            reverse("users:create"),
            data={
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword2",
            },
        )
        self.assertTemplateUsed(res, "base_form.html")


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")

    def test_profile_view_status_code(self):
        res = self.client.get(
            reverse("users:profile", kwargs={"username": self.user.username})
        )
        self.assertEqual(res.status_code, 200)


class ProfileEditViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser")

    def test_profile_edit_view_get(self):
        self.client.force_login(self.user)
        res = self.client.get(
            reverse(
                "users:profile_edit", kwargs={"username": self.user.username}
            )
        )
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "base_form.html")

    def test_profile_edit_view_post(self):
        self.client.force_login(self.user)
        res = self.client.post(
            reverse(
                "users:profile_edit", kwargs={"username": self.user.username}
            ),
            data={"bio": "test bio"},
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse("users:profile", kwargs={"username": self.user.username}),
        )

    def test_profile_edit_view_post_invalid(self):
        self.client.force_login(self.user)
        res = self.client.post(
            reverse(
                "users:profile_edit", kwargs={"username": self.user.username}
            ),
            data={"bio": "a" * (settings.BIO_MAX_LENGTH + 1)},
        )
        self.assertTemplateUsed(res, "base_form.html")


class UserPostsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a bunch of posts by a user
        cls.user = User.objects.create(username="testuser")

        for i in range(10):
            Post.objects.create(
                title=f"Test Post {i}",
                url=f"https://example.com/{i}",
                user=cls.user,
            )

    def test_user_posts_view_get(self):
        res = self.client.get(
            reverse("users:posts", kwargs={"username": self.user.username})
        )
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/posts.html")
        self.assertEqual(len(res.context["page_obj"]), 10)


class UserCommentsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a bunch of comments by a user
        cls.user = User.objects.create(username="testuser")

        for i in range(10):
            Comment.objects.create(
                body=f"test comment {i}",
                post=Post.objects.create(
                    title=f"Test Post {i}",
                    url=f"https://example.com/{i}",
                    user=cls.user,
                ),
                user=cls.user,
            )

    def test_user_comments_view_get(self):
        res = self.client.get(
            reverse("users:comments", kwargs={"username": self.user.username})
        )
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/comments.html")
        self.assertEqual(len(res.context["page_obj"]), 10)
