from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from .models import *

# Create your tests here.


class ProfessorModelTestCase(TestCase):

    fixtures = ["users.json", "professor.yaml"]

    def test_check_user1(self):

        professor: Professor = Professor.objects.get(id=1)
        self.assertEqual(professor.User.username, 'user1')
    
    def test_user_count(self):

        count = Professor.objects.all().count()

        self.assertEqual(count, 6)

class ProfessorAuthTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient(enforce_csrf_checks=True)
        cls.url_register = reverse('register')
        cls.url_login = reverse('login')
        cls.url_refresh = reverse('refresh')
        cls.update_first_name = 'Олег'
        cls.update_last_name = 'Филимонов'
        cls.update_location = 'nowhere'
        cls.update_phone = '88002233551'
        cls.user = User.objects.create_user(username='oleja', email='ol@mail.ru', password='hehe12345')
    
    def test_create_user(self):
        user_dict = {
            'username': 'test',
            'email': 'test@test.ru',
            'password': 'dgsghrseffs',
        }
        response = self.client.post(self.url_register, user_dict, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sign_up(self):
        user_dict = {
            'username': 'oleja',
            'password': 'hehe12345',
        }
        response = self.client.post(self.url_login, user_dict, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_refresh_token(self):
        user_dict = {
            'username': 'oleja',
            'password': 'hehe12345',
        }
        response_login = self.client.post(self.url_login, user_dict, format='json')
        access_token = response_login.data['access']
        refresh_token = response_login.data['refresh']
        response_refresh = self.client.post(self.url_refresh, {'refresh':refresh_token}, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response_refresh.data['access'], access_token)
    
    def test_userself(self):
        user_dict = {
            'username': 'oleja',
            'password': 'hehe12345',
        }
        response_login = self.client.post(self.url_login, user_dict, format='json')
        access_token = response_login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {access_token}')

        response = self.client.get('/api/users', data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
    

    def test_all_users(self):
        user_dict = {
            'username': 'oleja',
            'password': 'hehe12345',
        }
        response_login = self.client.post(self.url_login, user_dict, format='json')
        access_token = response_login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {access_token}')

        response = self.client.get('/api/all-users', data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
