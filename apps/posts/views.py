from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import PostSerializer


class PostCreationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def perform_create(self, serializer: PostSerializer) -> None:
        serializer.save(author=self.request.user)


post_creation = PostCreationView.as_view()
