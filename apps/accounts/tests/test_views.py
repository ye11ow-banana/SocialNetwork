from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

User = get_user_model()


class UserActivityViewTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.url = f'http://127.0.0.1:8000/api/accounts/{self.user.id}/activity/'

    def test_authentication_required(self) -> None:
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_required(self) -> None:
        user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        url = f'http://127.0.0.1:8000/api/accounts/{user2.id}/activity/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_required(self) -> None:
        self.user.is_staff = True
        self.user.save()
        user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        url = f'http://127.0.0.1:8000/api/accounts/{user2.id}/activity/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_existent_user(self) -> None:
        url = f'http://127.0.0.1:8000/api/accounts/{self.user.id+1}/activity/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_activity_is_valid(self) -> None:
        self.client.get(self.url)
        last_activity = str(self.user.last_activity)[:21].replace(' ', 'T')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data.keys()), 2)
        self.assertEqual(response.data['last_login'], self.user.last_login)
        self.assertEqual(response.data['last_activity'][:21], last_activity)
