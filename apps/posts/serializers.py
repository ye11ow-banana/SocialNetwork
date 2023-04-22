from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        exclude = ('author',)
        read_only_fields = ('date_created',)
