from django.urls import path
from .views import activate, registration, profile_page, edit_profile
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

# urlpatterns = [
#     path('registration/', UserRegisterView.as_view(), name='registration'),
# ]

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        activate, name='activate'),
    path('<int:pk>/profile/', profile_page, name='profile_page'),
    path('<int:pk>/profile/edit/', edit_profile, name='edit_profile'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)