from pathlib import Path

from rest_framework.generics import get_object_or_404

from django.db.models import Count, QuerySet
from django.db.models.functions import TruncDate
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


def get_post_with_id_or_404(post_id: int) -> Post:
    """
    Return `Post` object with loaded `id` field.
    """
    posts = Post.objects.filter(id=post_id).only('id')
    return get_object_or_404(posts)


def get_post_like_with_id_or_404(**kwargs) -> PostLike:
    """
    Return `PostLike` object with loaded `id` field.
    """
    post_likes = PostLike.objects.filter(**kwargs)
    return get_object_or_404(post_likes.only('id'))


def get_or_create_post_like(data: dict) -> tuple[PostLike, bool]:
    return PostLike.objects.get_or_create(**data)


def get_user_likes_by_day(
    user_id: int, date_from: str, date_to: str
) -> QuerySet[PostLike]:
    """
    Return how many likes was made by user aggregated by day.
    """
    likes = PostLike.objects.filter(author_id=user_id)
    if date_from is not None:
        likes = likes.filter(date_created__gte=date_from)
    if date_to is not None:
        likes = likes.filter(date_created__lte=date_to)
    likes = likes.annotate(day=TruncDate('date_created')).values('day')
    return likes.annotate(total_likes=Count('day'))
