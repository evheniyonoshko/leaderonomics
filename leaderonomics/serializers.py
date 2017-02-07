from django.contrib.auth.models import User
from rest_framework import serializers
from leaderonomics.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'leaderonomics')


class ArticlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Articles
        exclude = ('id',)
        read_only_fields = ('title', 'text')


class AuthenticatedArticlesSerializer(ArticlesSerializer):
    class Meta:
        model = Articles
        read_only_fields = ('id', 'title', 'text')