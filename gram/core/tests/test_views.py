from django.test import TestCase, Client
from django.urls import reverse
from ..models import Post, User
from django.core.files.uploadedfile import tempfile


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user2 = User.objects.create_user('john2', 'lennon@thebeatles2.com', 'johnpassword2')

    def test_feed_view_deny_anonymous_GET(self):
        response = self.client.get(reverse('feed'))
        self.assertRedirects(response, '/users/login/?next=/')
        self.assertEquals(response.status_code, 302)

    def test_feed_view_load_GET(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/feed.html')
        self.assertTrue('posts' in response.context)
        self.assertEqual(len(response.context['posts']), 0)

    def test_add_post_view_GET(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('add_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/add_post.html')

    def test_add_post_view_POST(self):
        self.client.login(username='john', password='johnpassword')
        self.assertEquals(Post.objects.filter(author=self.user1).count(), 0)
        response = self.client.post(reverse('add_post'),
                                    data={
                                        'title': 'Test Title',
                                        'tags': 'tag1',
                                        'image': tempfile.NamedTemporaryFile(suffix=".jpg").name
                                    })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.filter(author=self.user1).count(), 1)
        self.assertEquals(Post.objects.filter(author=self.user1).first().title, 'Test Title')

    def test_add_post_view_POST_not_valid(self):
        self.client.login(username='john2', password='johnpassword2')
        response = self.client.post(reverse('add_post'),
                                    data={
                                        'title': '',
                                        'tags': 'tag1',
                                        'image': tempfile.NamedTemporaryFile(suffix=".jpg").name
                                    })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.filter(author=self.user1).count(), 0)

    def test_like_post_view_POST_like(self):
        self.client.login(username='john', password='johnpassword')
        self.post = Post.objects.create(title='Test Title', author=self.user1)
        response = self.client.post(reverse('like_post'),
                                    data={'post_id': self.post.id})
        self.assertEquals(self.post.count_likes(), 1)
        self.assertEquals(response.status_code, 200)

    def test_like_post_view_POST_unlike(self):
        self.client.login(username='john', password='johnpassword')
        self.post = Post.objects.create(title='Test Title', author=self.user1)
        response1 = self.client.post(reverse('like_post'),
                                    data={'post_id': self.post.id})
        self.assertEquals(self.post.count_likes(), 1)
        response2 = self.client.post(reverse('like_post'),
                                    data={'post_id': self.post.id})
        self.assertEquals(self.post.count_likes(), 0)
        self.assertEquals(response2.status_code, 200)

    def test_tag_view(self):
        self.client.login(username='john', password='johnpassword')
        self.post = Post.objects.create(title='Test Title', tags='tag1', author=self.user1)
        response = self.client.get(reverse('posts_by_tag', kwargs={'tag_slug': 'tag1'}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/feed.html')
        self.assertEquals(response.context['first_post'], self.post)
