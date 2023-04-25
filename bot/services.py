import json
from datetime import date, timedelta
from random import randint

import requests


def signup(username: str, password: str) -> None:
    url = 'http://127.0.0.1:8000/api/accounts/auth/users/'
    data = dict(username=username, password=password)
    response = requests.post(url, data=data)
    if response.status_code != 201:
        raise ValueError(
            'Error has occurred during signup '
            f'Status code: {response.status_code}'
        )


def login(username: str, password: str) -> dict[str, str]:
    url = 'http://127.0.0.1:8000/api/accounts/auth/jwt/create/'
    data = dict(username=username, password=password)
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise ValueError(
            'Error has occurred during login '
            f'Status code: {response.status_code}'
        )
    return json.loads(response.text)


def create_post(text: str, access_token: str) -> dict:
    url = 'http://127.0.0.1:8000/api/posts/create/'
    headers = dict(Authorization=f'Bearer {access_token}')
    response = requests.post(url, data=dict(text=text), headers=headers)
    if response.status_code != 201:
        raise ValueError(
            'Error has occurred during creating text part of a post '
            f'Status code: {response.status_code}'
        )
    return json.loads(response.text)


def create_like(post_id: int, date_created: str, access_token: str) -> None:
    url = f'http://127.0.0.1:8000/api/posts/{post_id}/likes/add/'
    headers = dict(Authorization=f'Bearer {access_token}')
    response = requests.post(
        url, data=dict(date_created=date_created), headers=headers
    )
    if response.status_code != 201:
        raise ValueError(
            'Error has occurred during like creation. '
            f'Status code: {response.status_code}'
        )


def signup_users_and_create_posts(
    number_of_users: int, max_posts_per_user: int
) -> tuple[list[str], list[dict]]:
    access_tokens = []
    posts = []
    for _ in range(1, number_of_users + 1):
        username = f'username{_}'
        password = '!@#QWE!@#QWE'
        signup(username, password)
        access_token = login(username, password).get('access')
        if access_token is None:
            raise ValueError('Access token was not returned during login')
        access_tokens.append(access_token)
        for __ in range(randint(1, max_posts_per_user)):
            post = create_post(f'Some post text {__ + 1}', access_token)
            posts.append(post)
    return access_tokens, posts


def create_likes_randomly(
    access_tokens: list[str], posts: list[dict], max_likes_per_user: int
) -> None:
    for access_token in access_tokens:
        posts_copy = posts.copy()
        for __ in range(randint(0, max_likes_per_user)):
            post_index = 0
            if len(posts_copy) != 1:
                post_index = randint(0, len(posts_copy) - 1)
            post_id = posts_copy[post_index]['id']
            date_created = date.today() - timedelta(days=randint(1, 5))
            create_like(post_id, str(date_created), access_token)
            del posts_copy[post_index]
