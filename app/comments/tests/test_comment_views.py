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

    def test_create_reply_get(self):
        self.client.force_login(self.user)
        res = self.client.get(
            reverse("comments:reply", kwargs={"parent_id": self.comment.pk})
        )
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "comments/reply.html")
        self.assertIn("form", res.context)

    def test_create_reply_get_htmx(self):
        pass
        # FIXME htmx context not available
        # self.client.force_login(self.user)
        # res = self.client.get(
        #     reverse("comments:reply", kwargs={"parent_id": self.comment.pk}),
        #     {
        #         "commentFormEvent": "inlineFormPosted",
        #         "tree": "true",
        #     },
        #     headers={"HX-Request": "true"},
        # )
        # self.assertEqual(res.status_code, 200)
        # self.assertIn("form", res.context)
        # self.assertTemplateUsed(res, "comments/form.html")
        # self.assertIn("hx_attrs", res.context)

    def test_create_post_inline(self):
        self.client.force_login(self.user)
        res = self.client.post(
            reverse("comments:create"),
            {
                "body": "test comment",
                "post": self.post.pk,
                "tree": "true",
                "commentFormEvent": "inlineFormPosted",
            },
            headers={"HX-Request": "true"},
        )
        self.assertEqual(res.status_code, 201)
        self.assertTemplateUsed("comments/partials/tree.html#list-item")
        self.assertIn("inlineFormPosted", res.headers["HX-Trigger"])

    def test_create_post_invalid(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("comments:create"),
            data={"body": "", "post": self.post.pk},
        )
        # FIXME check for errors
        self.assertTemplateUsed("comments/form.html")

    def test_update_get(self):
        self.client.force_login(self.user)
        res = self.client.get(
            reverse("comments:update", kwargs={"pk": self.comment.pk})
        )
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "comments/form.html")
        self.assertIn("form", res.context)

    def test_update_get_htmx(self):
        pass
        # FIXME htmx context not available
        # self.client.force_login(self.user)
        # res = self.client.get(
        #     reverse("comments:update", kwargs={"pk": self.comment.pk}),
        #     {
        #         "commentFormEvent": "inlineFormPosted",
        #         "tree": "true",
        #     },
        #     headers={"HX-Request": "true"},
        # )
        # self.assertEqual(res.status_code, 200)
        # self.assertIn("form", res.context)
        # self.assertTemplateUsed(res, "comments/form.html")
