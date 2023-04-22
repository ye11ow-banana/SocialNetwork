from pathlib import Path

from django.conf import settings

from .models import Post


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
