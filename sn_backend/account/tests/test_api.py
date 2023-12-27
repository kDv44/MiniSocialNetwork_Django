from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User


class TestGetAccount(APITestCase):
    def test_get_account(self):
        url_me = reverse('me')
        url_signup = reverse('signup')
        url_login = reverse('token_obtain')
        data_signup = {
            "email": "Testantml@mail.com",
            "name": "TestAntony Ford",
            "password1": "!*(&passWord1",
            "password2": "!*(&passWord1",
        }
        data_login = {
            "email": f"{data_signup['email']}",
            "password": f"{data_signup['password1']}",
        }

        response_signup = self.client.post(url_signup, data_signup, format='json')
        self.assertEqual(response_signup.status_code, status.HTTP_200_OK)

        response_login = self.client.post(url_login, data_login, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

        token = response_login.data.get('access', None)
        self.assertIsNotNone(token, "Token not found in the login response.")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response_me = self.client.get(url_me)
        self.assertEqual(response_me.status_code, status.HTTP_200_OK)


class TestCreateAccount(APITestCase):
    def test_create_account(self):
        url = reverse('signup')
        data = {
            "email": "Testantml@mail.com",
            "name": "TestAntony Ford",
            "password1": "!*(&passWord1",
            "password2": "!*(&passWord1",
        }
        response_signup = self.client.post(url, data, format='json')
        self.assertEqual(response_signup.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, data["email"])
