from django.contrib.auth.models import User
from rest_framework import serializers
from leaderonomics.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'leaderonomics')


class AuthenticatedProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'birth', 'is_alumni')
        read_only_fields = ('id',)


class ArticlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Articles
        exclude = ('id',)
        read_only_fields = ('title', 'text')


class AuthenticatedArticlesSerializer(ArticlesSerializer):
    class Meta:
        model = Articles
        read_only_fields = ('id', 'title', 'text')


class VideosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Videos
        exclude = ('id',)
        read_only_fields = ('title', 'description', 'file')


class AuthenticatedVideosSerializer(ArticlesSerializer):
    class Meta:
        model = Videos
        read_only_fields = ('id', 'title', 'description', 'file')


class PodcastsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Podcasts
        exclude = ('id',)
        read_only_fields = ('title', 'file')


class AuthenticatedPodcastsSerializer(ArticlesSerializer):
    class Meta:
        model = Podcasts
        read_only_fields = ('id', 'title', 'file')

