from django.db import IntegrityError
from django.forms.forms import ValidationError
from django.test import TestCase
from django.urls import reverse

from app.posts.models import Post
from app.users.models import User

from ..models import Comment


class TestCommentModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser")
        cls.post = Post.objects.create(
            user=cls.user, title="test post", url="https://example.com"
        )

    def setUp(self):
        self.comment = Comment.objects.create(
            user=self.user, body="test comment", post=self.post
        )

    def test_save(self):
        c = Comment.objects.create(
            user=self.user, body="test comment", post=self.post
        )
        self.user.refresh_from_db()
        self.assertEqual(c.points, 0)
        self.assertEqual(self.user.points, 1)
        self.assertEqual(c.body, "test comment")
        self.assertEqual(c.post, self.post)

    def test_str(self):
        self.assertEqual(str(self.comment), f"{self.user}: test comment")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.comment.get_absolute_url(),
            reverse("comments:detail", kwargs={"pk": self.comment.pk}),
        )

    def test_get_post_url(self):
        self.assertEqual(
            self.comment.get_post_url(),
            reverse("posts:detail", kwargs={"pk": self.post.pk}),
        )

    def test_get_vote_url(self):
        self.assertEqual(
            self.comment.get_vote_url(),
            reverse("comments:vote", kwargs={"pk": self.comment.pk}),
        )

    def test_body_cannot_be_blank(self):
        with self.assertRaisesMessage(
            ValidationError, "This field cannot be blank."
        ):
            Comment.objects.create(
                user=self.user, body="", post=self.post
            ).clean_fields()

    def test_post_cannot_be_null(self):
        with self.assertRaises(IntegrityError):
            Comment.objects.create(
                user=self.user, body="test comment"
            ).clean_fields()

    def test_clean_no_error(self):
        Comment.objects.create(
            user=self.user, body="test comment", post=self.post
        ).full_clean()
