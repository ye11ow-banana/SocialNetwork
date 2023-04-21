from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def update_user_last_activity(pk: int) -> None:
    accounts = User.objects.filter(id=pk)
    accounts.update(last_activity=timezone.now())
