# Post, like, image
from django.test import TestCase
from ..models import Post, User


class TestCoreModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='TestingUsername1')
        user2 = User.objects.create_user(username='TestingUsername2')
        cls.post = Post.objects.create(title='Test Title', author=user1)
        cls.post.tags.add('tag1')
        cls.post.likes.set([user1.pk, user2.pk])

    def test_post_model_str(self):
        self.assertEqual(str(self.post), 'Test Title  |  by TestingUsername1')
        self.assertEqual(self.post.tags.count(), 1)

    def test_post_model_count_likes(self):
        self.assertEqual(self.post.count_likes(), 2)

    def test_like_model_str(self):
        self.assertEqual(str(self.post.likes.first()), 'TestingUsername1')

