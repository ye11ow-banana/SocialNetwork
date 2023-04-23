from rest_framework import serializers

from . import services
from .models import Post, Media, PostLike


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        exclude = ('author',)
        read_only_fields = ('date_created',)


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ('file',)

    def create(self, validated_data: dict) -> Media:
        file = validated_data['file']
        validated_data['type'] = services.get_media_type(file.name)
        return Media.objects.create(**validated_data)


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        exclude = ('post', 'author')

    def create(self, validated_data: dict) -> PostLike:
        post_like, _ = services.get_or_create_post_like(validated_data)
        return post_like
