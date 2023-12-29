from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User

universal_data_json = {
    "email": "Testantml@mail.com",
    "name": "TestAntony Ford",
    "password1": "!*(&passWord1",
    "password2": "!*(&passWord1",
}

friend_data_json = {
    "email": "friendTestantml@mail.com",
    "name": "TestAntony SDFord",
    "password1": "!*(&passWord1",
    "password2": "!*(&passWord1",
}


# test - def me
class TestGetAccount(APITestCase):
    def test_get_account(self):
        url_me = reverse("me")
        url_signup = reverse("signup")
        url_login = reverse("token_obtain")
        data_signup = universal_data_json
        data_login = {
            "email": f"{data_signup['email']}",
            "password": f"{data_signup['password1']}",
        }

        response_signup = self.client.post(url_signup, data_signup, format="json")
        self.assertEqual(response_signup.status_code, status.HTTP_200_OK)

        response_login = self.client.post(url_login, data_login, format="json")
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

        token = response_login.data.get("access")
        self.assertIsNotNone(token, "Token not found in the login response.")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response_me = self.client.get(url_me)
        self.assertEqual(response_me.status_code, status.HTTP_200_OK)


# test - def signup
class TestCreateAccount(APITestCase):
    def test_create_account(self):
        url = reverse("signup")
        data = universal_data_json
        response_signup = self.client.post(url, data, format="json")
        self.assertEqual(response_signup.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, data["email"])


# test - def send_friendship_request
class TestSendFriendRequest(APITestCase):
    def test_friend_request(self):
        url_me = reverse("me")
        url_signup = reverse("signup")
        url_login = reverse("token_obtain")

        main_data_signup = universal_data_json

        friend_data = friend_data_json
        friend_data_login = {
            "email": f"{main_data_signup['email']}",
            "password": f"{main_data_signup['password1']}",
        }

        response_signup_main = self.client.post(url_signup, main_data_signup, format="json")
        self.assertEqual(response_signup_main.status_code, status.HTTP_200_OK)

        response_signup_friend = self.client.post(url_signup, friend_data, format="json")
        self.assertEqual(response_signup_friend.status_code, status.HTTP_200_OK)

        response_friend_login = self.client.post(url_login, friend_data_login, format="json")
        self.assertEqual(response_friend_login.status_code, status.HTTP_200_OK)

        token = response_friend_login.data.get("access")
        self.assertIsNotNone(token, "Token not found in the login response.")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response_me = self.client.get(url_me)
        self.assertEqual(response_me.status_code, status.HTTP_200_OK)

        friend_id = response_me.get("id")
        url_friend_request = f"http://127.0.0.1:8000/api/friends/{friend_id}/request/"

        self.client.post(url_friend_request)


