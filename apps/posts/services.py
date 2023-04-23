from pathlib import Path

from rest_framework.generics import get_object_or_404

from django.conf import settings

from .models import Post, PostLike


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix[1:].lower()


def get_media_type(filename: str) -> str:
    """
    Return `type` field of `Media` model given the extension.
    """
    extension = get_file_extension(filename)
    return 'video' if extension in settings.VIDEO_FORMATS else 'image'


def check_user_is_post_author(post_id: int, user_id: int) -> bool:
    return Post.objects.filter(id=post_id, author_id=user_id).exists()


def get_post_or_404(post_id: int) -> Post:
    posts = Post.objects.filter(id=post_id)
    return get_object_or_404(posts)


def get_or_create_post_like(data: dict) -> tuple[PostLike, bool]:
    return PostLike.objects.get_or_create(**data)
