from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

from .models import Post


class PostListTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(
            "testuser",
            "test@user.com",
            "secretpassword",
        )
        Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.author,
            status="published",
        )

    def test_post_list(self):
        """ """
        response = self.client.get("/blog/")
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the rendered context contains 1 post.
        self.assertEqual(len(response.context["posts"]), 1)

    def test_post_list_context(self):
        """ """
        Post.objects.create(
            title="Test Post 1",
            slug="test-post-1",
            author=self.author,
            status="published",
        )
        Post.objects.create(
            title="Test Post 2",
            slug="test-post-2",
            author=self.author,
            status="published",
        )
        Post.objects.create(
            title="Test Post 3",
            slug="test-post-3",
            author=self.author,
            status="draft",
        )
        response = self.client.get("/blog/")
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the rendered context contains 1 post.
        self.assertEqual(len(response.context["posts"]), 3)

    def test_post_detail(self):
        """ """
        today = timezone.now()
        today = today.strftime("%Y/%m/%d")

        response = self.client.get(f"/blog/{today}/test-post/")
        self.assertEqual(response.status_code, 200)

    def test_post_detail_context(self):
        Post.objects.create(
            title="Test Post 2",
            slug="test-post-2",
            author=self.author,
            status="published",
        )

        Post.objects.create(
            title="Test Post 3",
            slug="test-post-3",
            author=self.author,
            status="draft",
        )
        today = timezone.now()
        today = today.strftime("%Y/%m/%d")

        response = self.client.get(f"/blog/{today}/test-post/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"/blog/{today}/test-post-2/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"/blog/{today}/test-post-3/")
        self.assertEqual(response.status_code, 404)
