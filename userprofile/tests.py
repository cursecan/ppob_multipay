from django.test import TestCase
from django.test import Client

# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Wallet

class TestingProfileModel(TestCase):
    def add_user_test(self):
        self.user_obj = User.objects.create_user('user1@user.com', 'user1@user.com', 'toor#123')
    
    def login_test(self):
        self.client = Client()
        self.client.login(username='user1@user.com', password='toor#123')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    