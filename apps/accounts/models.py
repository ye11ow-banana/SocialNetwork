from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    """
    Main user model in the project.
    """

    last_activity = models.DateTimeField(
        'User last request', auto_now_add=True, blank=True)

    class Meta:
        db_table = 'account'
