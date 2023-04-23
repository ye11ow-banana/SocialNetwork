from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.http import Http404

from . import services
from .models import PostLike
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
        post = services.get_post_with_id_or_404(post_pk)
        serializer.save(author=self.request.user, post=post)


class PostLikeDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        post_pk = self.kwargs['pk']
        return services.get_post_like_with_id_or_404(
            author_id=self.request.user.id, post_id=post_pk
        )

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)


post_creation = PostCreationView.as_view()
media_creation = MediaCreationView.as_view()
post_like_creation = PostLikeCreationView.as_view()
post_like_destroy = PostLikeDestroyView.as_view()
