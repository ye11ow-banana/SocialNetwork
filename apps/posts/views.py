from rest_framework import generics
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated

from .permissions import IsPostAuthor
from .serializers import PostSerializer, MediaSerializer


class PostCreationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def perform_create(self, serializer: PostSerializer) -> None:
        serializer.save(author=self.request.user)


class MediaCreationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]
    serializer_class = MediaSerializer
    parser_classes = [FileUploadParser]

    def perform_create(self, serializer: MediaSerializer) -> None:
        post_id = self.kwargs['pk']
        serializer.save(post_id=post_id)


post_creation = PostCreationView.as_view()
media_creation = MediaCreationView.as_view()
