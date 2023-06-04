from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from .models import Post


class BlogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='aryo', password='aryo')
        cls.post = Post.objects.create(title="hama", text="description", status="pub", author=cls.user)
        cls.draft_post = Post.objects.create(
            title="notpublished",
            text="im here to test published or draft post",
            status=Post.STATUS_CHOICES[1][0],
            author=cls.user
        )

    def test_post_str(self):
        post = self.post
        self.assertEqual(str(post), post.title)

    def test_post_detail(self):
        self.assertEqual(self.post.title, "hama")
        self.assertEqual(self.post.text, "description")

    def test_list_view(self):
        respond = self.client.get("/post/")
        self.assertEqual(respond.status_code, 200)

    def test_list_view_by_name(self):
        respond = self.client.get(reverse("post_list"))
        self.assertEqual(respond.status_code, 200)

    def test_obj_in_list_view(self):
        response = self.client.get(reverse("post_list"))
        self.assertContains(response, self.post.title)

    def test_post_detail_view(self):
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_by_name(self):
        response = self.client.get(reverse("post_detail", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

    def test_obj_in_detail_view(self):
        response = self.client.get(f"/post/{self.post.id}/")
        self.assertContains(response, self.post.title)

    def test_obj_or_404_in_post_detail_view(self):
        response = self.client.get(reverse("post_detail", args=[self.post.id]))
        self.assertNotContains(response, not self.post.title)
        self.assertNotContains(response, not self.post.text)

    def test_404_post_detail_view(self):
        response = self.client.get(reverse("post_detail", args=[1000]))
        self.assertEqual(response.status_code, 404)

    def test_obj_status_is_published(self):
        response = self.client.get(reverse("post_list"))
        self.assertContains(response, self.post.title)
        self.assertNotContains(response, self.draft_post.title)

    def test_post_create_view(self):
        response = self.client.post(reverse("post_create"), {
            "title": "some title",
            "text": "some text",
            "status": "pub",
            "author": self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "some title")
        self.assertEqual(Post.objects.last().text, "some text")

    def test_post_update_view(self):
        response = self.client.post(reverse("post_update", args=[self.draft_post.id]), {
            "title": "title updated",
            "text": "text updated",
            "status": "pub",
            "author": self.draft_post.author.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "title updated")
        self.assertEqual(Post.objects.last().text, "text updated")

    def test_post_delete_view(self):
        response = self.client.post(reverse("post_delete", args=[self.draft_post.id]))
        self.assertEqual(response.status_code, 302)

