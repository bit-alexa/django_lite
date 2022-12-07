from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django_currentuser.db.models import CurrentUserField
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = CurrentUserField(on_delete=models.CASCADE)
    post_date = models.DateField(auto_now_add=True)
    tags = TaggableManager()
    likes = models.ManyToManyField(User, default=None, blank=True, related_name='likes')

    def __str__(self):
        return self.title + '  |  by ' + str(self.author)

    def count_likes(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=settings.LIKE_CHOICES, default='Like', max_length=10)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="images/posts/")
