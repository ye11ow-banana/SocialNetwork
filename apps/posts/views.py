from rest_framework import generics
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated

from . import services
from .permissions import IsPostAuthor
from .serializers import PostSerializer, MediaSerializer, PostLikeSerializer


class PostCreationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MediaCreationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]
    serializer_class = MediaSerializer
    parser_classes = [FileUploadParser]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(post_id=post_id)


class PostLikeCreationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostLikeSerializer

    def perform_create(self, serializer):
        post_pk = self.kwargs['pk']
        post = services.get_post_or_404(post_pk)
        serializer.save(author=self.request.user, post=post)


post_creation = PostCreationView.as_view()
media_creation = MediaCreationView.as_view()
post_like_creation = PostLikeCreationView.as_view()
