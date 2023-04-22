import json

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from posts.models import Post

User = get_user_model()


class PostCreationViewTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.url = 'http://127.0.0.1:8000/api/posts/create/'

    def test_authentication_required(self) -> None:
        self.client.credentials()
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_empty_data(self) -> None:
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().text, None)
        self.assertEqual(Post.objects.first().author, self.user)

    def test_new_post_created(self) -> None:
        self.user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        data = json.dumps(dict(text='Test Text'))
        response = self.client.post(
            self.url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().text, 'Test Text')
        self.assertEqual(Post.objects.first().author, self.user)
