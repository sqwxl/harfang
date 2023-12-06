from django.test import TestCase
from django.urls import reverse
from app.comments.models import Comment

from app.posts.models import Post
from app.users.models import User


class CommentViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser")
        cls.post = Post.objects.create(
            user=cls.user, title="test post", url="https://example.com"
        )
        cls.comment = Comment.objects.create(
            user=cls.user, post=cls.post, body="test comment"
        )

    def test_create_get(self):
        self.client.force_login(self.user)
        res = self.client.get(reverse("comments:create"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "comments/form.html")

    def test_create_post(self):
        self.client.force_login(self.user)
        res = self.client.post(
            reverse("comments:create"),
            data={"body": "test comment", "post": self.post.pk},
        )
        self.assertEqual(res.status_code, 201)
        self.assertTemplateUsed("comments/partials/article.html")

    def test_create_post_reply(self):
        self.client.force_login(self.user)
        res = self.client.post(
            reverse("comments:create"),
            data={
                "body": "test comment",
                "post": self.post.pk,
                "parent": self.comment.pk,
            },
        )
        self.assertEqual(res.status_code, 201)
        self.assertTemplateUsed("comments/partials/tree.html")
