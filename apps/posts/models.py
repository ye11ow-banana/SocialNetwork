from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

User = settings.AUTH_USER_MODEL


class Post(models.Model):
    """
    Representation of a post in a social
    network with text and media.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Post author',
    )
    date_created = models.DateTimeField(
        'Post creation date', auto_now_add=True)
    text = models.CharField(
        'Post text', max_length=9999, blank=True, null=True)

    class Meta:
        db_table = 'post'


class Media(models.Model):
    """
    Photo or video attached to a post.
    """

    MEDIA_CHOICES = (
        ('image', 'image'),
        ('video', 'video'),
    )

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='medias'
    )
    file = models.FileField(
        upload_to='posts/%Y/%m/%d',
        validators=[FileExtensionValidator(
            allowed_extensions=settings.IMAGE_FORMATS + settings.VIDEO_FORMATS
        )],
    )
    type = models.CharField(
        choices=MEDIA_CHOICES, max_length=5, default='image')

    class Meta:
        db_table = 'media'


class PostLike(models.Model):
    """
    User like for a post.
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Liked post',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Like owner',
    )

    class Meta:
        db_table = 'like'
        unique_together = ('post', 'author')
