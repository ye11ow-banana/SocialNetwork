from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsCurrentUser(BasePermission):
    """
    Allows access to user who is user from url user_pk.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.id == view.kwargs['pk']


class IsStaff(BasePermission):

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_staff
