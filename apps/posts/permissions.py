from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from . import services


class IsPostAuthor(BasePermission):
    """
    Allows access only to the author of the post.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        pk = view.kwargs['pk']
        user = request.user
        return services.check_user_is_post_author(pk, user.id)
