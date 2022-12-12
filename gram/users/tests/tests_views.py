from django.core.serializers import json
from django.test import TestCase, Client
from django.urls import reverse
import mock
from core.models import Post, Image, User




class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user2 = User.objects.create_user('john2', 'lennon@thebeatles2.com', 'johnpassword2')

    def test_registration_view(self):
        response = self.client.post(reverse('registration'),
                                    data={'email': 'lobachovaalexandra@gmail.com',
                                          'username': 'usernnametest',
                                          'password1': 'dkfjnfd6H',
                                          'password2': 'dkfjnfd6H'}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Please confirm your email address to complete the registration')

    def test_activate_view(self):
        response = self.client.get(reverse('activate', kwargs={'uidb64': 'mockingtoken', 'token': 'mokingtoken'}))
        self.assertEquals(response.status_code, 200)

    def test_profile_page_view(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('profile_page', args='1'))
        self.assertEquals(response.status_code, 200)

    def test_edit_profile_GET(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('edit_profile', args='1'))
        self.assertEquals(response.status_code, 200)

    def test_edit_profile_POST(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse('edit_profile', args=str(self.user1.pk)),
                         data={'bio': 'somebio'})
        self.assertEquals(response.status_code, 200)











