from django.contrib.auth.models import Group
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

    def test_post_clean_no_error(self):
        # test that a post with a url but no body is valid
        self.post.body = ""
        self.post.clean()

    def test_post_clean_no_error_2(self):
        # test that a post with a body but no url is valid
        self.post.url = ""
        self.post.clean()


class PostDetailViewTest(TestCase):
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

    def test_post_detail_view(self):
        # test that the detail view returns a 200
        resp = self.client.get(self.post.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_post_detail_view_template(self):
        # test that the detail view uses the correct template
        resp = self.client.get(self.post.get_absolute_url())
        self.assertTemplateUsed(resp, "posts/detail.html")

    def test_post_detail_view_context(self):
        # test that the detail view returns the correct context
        resp = self.client.get(self.post.get_absolute_url())
        self.assertEqual(resp.context["post"], self.post)

    def test_post_detail_view_context_no_comments(self):
        # test that the detail view returns the correct context when there are no comments
        resp = self.client.get(self.post.get_absolute_url())
        self.assertFalse(resp.context["comments"])

    def test_post_detail_view_context_with_comments(self):
        # test that the detail view returns the correct context when there are comments
        self.post.comments.create(body="Test Comment", user=self.user)
        resp = self.client.get(self.post.get_absolute_url())
        self.assertEqual(resp.context["comments"].count(), 1)


class PostCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser")

    def test_post_create_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("posts:submit"))
        self.assertEqual(resp.status_code, 200)

    def test_post_create_view_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("posts:submit"))
        self.assertTemplateUsed(resp, "base_form.html")

    def test_post_create_view_redirects(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse("posts:submit"),
            {
                "title": "Test Post",
                "body": "Test Body",
                "url": "http://test.com/",
            },
        )
        self.assertRedirects(resp, reverse("posts:detail", kwargs={"pk": 1}))

    def test_post_create_view_creates_post(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("posts:submit"),
            {
                "title": "Test Post",
                "body": "Test Body",
                "url": "http://test.com/",
            },
        )
        self.assertEqual(Post.objects.count(), 1)

    def test_post_create_view_creates_post_with_correct_data(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("posts:submit"),
            {
                "title": "Test Post",
                "body": "Test Body",
                "url": "http://test.com/",
            },
        )
        p = Post.objects.first()
        self.assertEqual(p.title, "Test Post")
        self.assertEqual(p.body, "Test Body")
        self.assertEqual(p.url, "http://test.com/")
        self.assertEqual(p.user, self.user)

    def test_post_create_view_does_not_create_post_when_form_invalid(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("posts:submit"),
            {
                "title": "",
                "body": "",
                "url": "",
            },
        )
        self.assertEqual(Post.objects.count(), 0)

    def test_post_create_view_returns_422_when_form_invalid(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse("posts:submit"),
            {
                "title": "",
                "body": "",
                "url": "",
            },
        )
        self.assertEqual(resp.status_code, 422)

    def test_post_create_view_returns_form_with_errors_when_form_invalid(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse("posts:submit"),
            {
                "title": "",
                "body": "",
                "url": "",
            },
        )
        self.assertTrue(resp.context["form"])
        self.assertTrue(resp.context["form"].errors)


class TestPostUpdateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser")
        cls.post = Post.objects.create(
            title="Test Post",
            body="Test Body",
            url="http://test.com/",
            user=cls.user,
        )

    def test_post_update_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse("posts:update", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(resp.status_code, 200)

    def test_post_update_view_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse("posts:update", kwargs={"pk": self.post.pk})
        )
        self.assertTemplateUsed(resp, "base_form.html")

    def test_post_update_view_redirects(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse("posts:update", kwargs={"pk": self.post.pk}),
            {
                "title": "Test Post 2",
                "body": "Test Body 2",
                "url": "http://test2.com/",
            },
        )
        self.assertRedirects(resp, self.post.get_absolute_url())

    def test_post_update_view_updates_post(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("posts:update", kwargs={"pk": self.post.pk}),
            {
                "title": "Test Post 2",
                "body": "Test Body 2",
                "url": "http://test2.com/",
            },
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Test Post 2")
        self.assertEqual(self.post.body, "Test Body 2")
        self.assertEqual(self.post.url, "http://test2.com/")

    def test_post_update_view_does_not_update_post_when_form_invalid(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("posts:update", kwargs={"pk": self.post.pk}),
            {
                "title": "",
                "body": "",
                "url": "",
            },
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.body, "Test Body")
        self.assertEqual(self.post.url, "http://test.com/")

    def test_post_update_view_returns_422_when_form_invalid(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse("posts:update", kwargs={"pk": self.post.pk}),
            {
                "title": "",
                "body": "",
                "url": "",
            },
        )
        self.assertEqual(resp.status_code, 422)

    def test_post_update_view_returns_form_with_errors_when_form_invalid(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse("posts:update", kwargs={"pk": self.post.pk}),
            {
                "title": "",
                "body": "",
                "url": "",
            },
        )
        self.assertTrue(resp.context["form"])
        self.assertTrue(resp.context["form"].errors)


class TestPostDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser")
        cls.post = Post.objects.create(
            title="Test Post",
            body="Test Body",
            url="http://test.com/",
            user=cls.user,
        )

    def test_post_delete_view_redirects_anonymous_user(self):
        resp = self.client.post(
            reverse("posts:delete", kwargs={"pk": self.post.pk}),
        )
        self.assertRedirects(resp, reverse("login") + "?next=/posts/1/delete/")

    def test_post_delete_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse("posts:delete", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(resp.status_code, 200)

    def test_post_delete_view_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse("posts:delete", kwargs={"pk": self.post.pk})
        )
        self.assertTemplateUsed(resp, "posts/delete.html")

    def test_post_delete_view_redirects(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse("posts:delete", kwargs={"pk": self.post.pk}),
        )
        self.assertEqual(resp.status_code, 302)

    def test_post_delete_view_deletes_post(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("posts:delete", kwargs={"pk": self.post.pk}),
        )
        self.assertEqual(Post.objects.count(), 0)

    def test_post_delete_view_returns_403_when_user_is_not_author(self):
        user = User.objects.create(username="testuser2")
        self.client.force_login(user)
        resp = self.client.post(
            reverse("posts:delete", kwargs={"pk": self.post.pk}),
        )
        self.assertEqual(resp.status_code, 403)

    def test_post_delete_view_does_not_delete_post_when_user_is_not_author(
        self
    ):
        user = User.objects.create(username="testuser2")
        self.client.force_login(user)
        self.client.post(
            reverse("posts:delete", kwargs={"pk": self.post.pk}),
        )
        self.assertEqual(Post.objects.count(), 1)

    def test_post_delete_view_deletes_post_when_user_is_not_author_but_moderator(
        self
    ):
        user = User.objects.create(username="testuser2")
        group = Group.objects.create(name="Moderator")
        user.groups.add(group)
        self.client.force_login(user)
        self.client.post(
            reverse("posts:delete", kwargs={"pk": self.post.pk}),
        )
        self.assertEqual(Post.objects.count(), 0)

    def test_post_delete_view_deletes_post_when_user_is_not_author_but_staff(
        self
    ):
        user = User.objects.create(username="testuser2")
        # make user staff
        user.is_staff = True
        user.save()
        self.client.force_login(user)
        self.client.post(
            reverse("posts:delete", kwargs={"pk": self.post.pk}),
        )
        self.assertEqual(Post.objects.count(), 0)


class TestPostVoteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser")
        cls.post = Post.objects.create(
            title="Test Post",
            body="Test Body",
            url="http://test.com/",
            user=cls.user,
        )

    def test_post_vote_view_redirects_anonymous_user(self):
        resp = self.client.post(
            reverse("posts:vote", kwargs={"pk": self.post.pk}),
        )
        self.assertRedirects(resp, reverse("login") + "?next=/posts/1/vote/")

    def test_post_vote_view_rejects_get_request(self):
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse("posts:vote", kwargs={"pk": self.post.pk}),
        )
        self.assertEqual(resp.status_code, 405)

    def test_post_vote_view_prevents_user_from_voting_on_own_post(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse("posts:vote", kwargs={"pk": self.post.pk}),
        )
        self.assertEqual(resp.status_code, 403)

    def test_post_vote_view_creates_vote(self):
        user = User.objects.create(username="testuser2")
        self.client.force_login(user)
        resp = self.client.post(
            reverse("posts:vote", kwargs={"pk": self.post.pk}),
        )
        self.assertEqual(self.post.votes.count(), 1)
        self.assertEqual(resp.status_code, 201)

    def test_post_vote_view_deletes_vote_when_user_already_voted(self):
        user = User.objects.create(username="testuser2")
        self.client.force_login(user)
        self.client.post(
            reverse("posts:vote", kwargs={"pk": self.post.pk}),
        )
        resp = self.client.post(
            reverse("posts:vote", kwargs={"pk": self.post.pk}),
        )
        self.assertEqual(self.post.votes.count(), 0)
        self.assertEqual(resp.status_code, 200)

    def test_post_vote_view_uses_correct_template(self):
        user = User.objects.create(username="testuser2")
        self.client.force_login(user)
        resp = self.client.post(
            reverse("posts:vote", kwargs={"pk": self.post.pk}),
        )
        self.assertTemplateUsed(resp, "partials/vote.html")
