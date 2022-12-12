from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django_currentuser.db.models import CurrentUserField
from cloudinary.models import CloudinaryField


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


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/posts/")
