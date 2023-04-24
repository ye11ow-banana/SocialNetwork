import json
import shutil

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from posts.models import Post, Media, PostLike

User = get_user_model()
TEST_DIR = 'tmp'


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
        post = Post.objects.first()
        self.assertEqual(post.text, None)
        self.assertEqual(post.author, self.user)

    def test_new_post_created(self) -> None:
        self.user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        data = json.dumps(dict(text='Test Text'))
        response = self.client.post(
            self.url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.text, 'Test Text')
        self.assertEqual(post.author, self.user)


class MediaCreationViewTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.post = Post.objects.create(author=self.user)
        self.url = f'http://127.0.0.1:8000/api/posts/{self.post.id}/media/add/'

    def test_authentication_required(self) -> None:
        self.client.credentials()
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_author_required(self) -> None:
        self.user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        self.post.author = self.user2
        self.post.save()
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_new_media_created_with_image_type(self) -> None:
        file = SimpleUploadedFile('file.jpg', b'file_content')
        response = self.client.post(
            self.url, data=file.read(), content_type='image.jpeg',
            headers={'Content-Disposition': 'attachment; filename=file.jpg'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Media.objects.count(), 1)
        media = Media.objects.first()
        self.assertEqual(media.post, self.post)
        self.assertEqual(media.type, 'image')
        self.assertEqual(media.file.read(), b'file_content')

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_new_media_created_with_video_type(self) -> None:
        file = SimpleUploadedFile('file.mp4', b'file_content')
        response = self.client.post(
            self.url, data=file.read(), content_type='video/mp4',
            headers={'Content-Disposition': 'attachment; filename=file.mp4'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Media.objects.count(), 1)
        media = Media.objects.first()
        self.assertEqual(media.post, self.post)
        self.assertEqual(media.type, 'video')
        self.assertEqual(media.file.read(), b'file_content')

    def test_new_media_with_wrong_extension(self) -> None:
        file = SimpleUploadedFile('file.gif', b'file_content')
        response = self.client.post(
            self.url, data=file.read(), content_type='image/gif',
            headers={'Content-Disposition': 'attachment; filename=file.gif'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Media.objects.count(), 0)

    def test_empty_data(self) -> None:
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Media.objects.count(), 0)

    def tearDown(self) -> None:
        """
        Delete `TEST_DIR` after test functions working with files.
        """
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass


class PostLikeCreationViewTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.post = Post.objects.create(author=self.user)
        self.url = f'http://127.0.0.1:8000/api/posts/{self.post.id}/likes/add/'

    def test_authentication_required(self) -> None:
        self.client.credentials()
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_new_post_like_created(self) -> None:
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(PostLike.objects.count(), 1)
        post_like = PostLike.objects.first()
        self.assertEqual(post_like.author, self.user)
        self.assertEqual(post_like.post, self.post)

    def test_non_existent_post(self) -> None:
        url = f'http://127.0.0.1:8000/api/posts/{self.post.id+1}/likes/add/'
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(PostLike.objects.count(), 0)

    def test_second_like_rejected(self) -> None:
        PostLike.objects.create(author=self.user, post=self.post)
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(PostLike.objects.count(), 1)
        post_like = PostLike.objects.first()
        self.assertEqual(post_like.author, self.user)
        self.assertEqual(post_like.post, self.post)


class PostLikeDestroyViewTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.post = Post.objects.create(author=self.user)
        self.post_like = PostLike.objects.create(
            author=self.user, post=self.post
        )
        self.url = f'http://127.0.0.1:8000/api/posts/' \
                   f'{self.post.id}/likes/remove/'

    def test_authentication_required(self) -> None:
        self.client.credentials()
        response = self.client.delete(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_like_of_someone_else_post_destroyed(self) -> None:
        """
        Checks that `PostLike` object will be destroyed even
        if the author of `Post` object is someone else.
        """
        self.user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        self.post.author = self.user2
        self.post.save()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(PostLike.objects.count(), 0)

    def test_post_like_destroyed(self) -> None:
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(PostLike.objects.count(), 0)

    def test_non_existent_post(self) -> None:
        url = f'http://127.0.0.1:8000/api/posts/' \
                f'{self.post.id+1}/likes/remove/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(PostLike.objects.count(), 1)

    def test_non_existent_post_like(self) -> None:
        self.post_like.delete()
        url = f'http://127.0.0.1:8000/api/posts/{self.post.id}/likes/remove/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(PostLike.objects.count(), 0)


class LikeAnalyticsViewTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test_user', password='test_pass')
        self.user2 = User.objects.create_user(
            username='test_user2', password='test_pass2')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer  {self.token}')
        self.url = 'http://127.0.0.1:8000/api/posts/likes/analytics/'
        self.post = Post.objects.create(author=self.user)
        self.post2 = Post.objects.create(author=self.user2)
        self.post3 = Post.objects.create(author=self.user)
        self.post_like1 = PostLike.objects.create(
            author=self.user, post=self.post, date_created='2023-10-10')
        self.post_like2 = PostLike.objects.create(
            author=self.user2, post=self.post, date_created='2023-10-10')
        self.post_like3 = PostLike.objects.create(
            author=self.user, post=self.post2, date_created='2023-05-10')
        self.post_like4 = PostLike.objects.create(
            author=self.user, post=self.post3, date_created='2023-10-10')

    def test_authentication_required(self) -> None:
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_empty_query_params(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(PostLike.objects.count(), 4)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['day'], '2023-05-10')
        self.assertEqual(response.data[0]['total_likes'], 1)
        self.assertEqual(response.data[1]['day'], '2023-10-10')
        self.assertEqual(response.data[1]['total_likes'], 2)

    def test_data_range_query_params(self) -> None:
        url = f'{self.url}?date_from=2023-05-10&date_to=2023-10-09'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(PostLike.objects.count(), 4)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['day'], '2023-05-10')
        self.assertEqual(response.data[0]['total_likes'], 1)

    def test_pagination(self) -> None:
        url = f'{self.url}?limit=1&offset=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(PostLike.objects.count(), 4)
        data = response.data['results']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['day'], '2023-10-10')
        self.assertEqual(data[0]['total_likes'], 2)
