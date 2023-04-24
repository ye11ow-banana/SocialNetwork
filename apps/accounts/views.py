from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from django.contrib.auth import get_user_model

from .permissions import IsCurrentUser, IsStaff
from .serializers import UserActivitySerializer

User = get_user_model()


class UserActivityView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsCurrentUser | IsStaff]
    serializer_class = UserActivitySerializer
    queryset = User.objects


user_activity = UserActivityView.as_view()
