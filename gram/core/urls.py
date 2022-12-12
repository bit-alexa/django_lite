from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import feed, add_post, TagView, like_post

urlpatterns = [
    path('', feed, name='feed'),
    path('add_post/', add_post, name='add_post'),
    path('tag/<slug:tag_slug>/', login_required(TagView.as_view()), name='posts_by_tag'),
    path('like/', like_post, name='like_post'),
    path('pers/<slug:personal_feed>/', feed, name='personal_feed'),
]
