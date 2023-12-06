from django.test import TestCase
from django.test.utils import override_settings
from app.posts.models import Post

from app.users.models import User

from ..forms import CommentForm


class CommentFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(
            user=User.objects.create(username="testuser"),
            title="test post",
            url="https://example.com",
        )

    def test_valid(self):
        form = CommentForm(data={"body": "test comment", "post": self.post.pk})
        self.assertTrue(form.is_valid(), form.errors)

    def test_honeypot(self):
        form = CommentForm(
            data={"body": "test comment", "post": self.post.pk, "honeypot": "a"}
        )
        self.assertFalse(form.is_valid())

    @override_settings(PROFANITIES_LIST=["poopoo"])
    def test_profanities(self):
        with self.settings(COMMENTS_BLOCK_PROFANITIES=False):
            form = CommentForm(data={"body": "poopoo", "post": self.post.pk})
            self.assertTrue(form.is_valid())
        with self.settings(COMMENTS_BLOCK_PROFANITIES=True):
            form = CommentForm(data={"body": "poopoo", "post": self.post.pk})
            self.assertFalse(form.is_valid())
