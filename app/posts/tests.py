from django.forms.forms import ValidationError
from django.test import TestCase
from django.urls import reverse

from app.users.models import User
from .models import Post


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser")

    def setUp(self):
        self.post = Post.objects.create(
            title="Test Post",
            body="Test Body",
            url="http://test.com/",
            user=self.user,
        )

    def test_post_str(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_post_get_absolute_url(self):
        self.assertEqual(
            self.post.get_absolute_url(),
            reverse("posts:detail", kwargs={"pk": self.post.pk}),
        )

    def test_post_get_vote_url(self):
        self.assertEqual(
            self.post.get_vote_url(),
            reverse("posts:vote", kwargs={"pk": self.post.pk}),
        )

    def test_post_save_increments_user_points(self):
        # test that creating a post increments the user's points
        self.user.refresh_from_db()
        curr_points = self.user.points
        Post.objects.create(
            title="Test Post",
            body="Test Body",
            url="http://test.com/",
            user=self.user,
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.points, curr_points + 1)

    def test_post_delete_decrements_user_points(self):
        # test that deleting a post decrements the user's points
        p = Post.objects.create(
            title="Test Post",
            body="Test Body",
            url="http://test.com/",
            user=self.user,
        )
        self.user.refresh_from_db()
        curr_points = self.user.points
        p.delete()
        self.user.refresh_from_db()
        self.assertEqual(self.user.points, curr_points - 1)

    def test_post_clean(self):
        # test that a post must have either a url or body
        self.post.url = ""
        self.post.body = ""
        with self.assertRaises(ValidationError):
            self.post.clean()
