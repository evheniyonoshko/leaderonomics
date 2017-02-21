from django.contrib.auth.models import User
from rest_framework import serializers
from leaderonomics.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'leaderonomics')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'birth', 'is_alumni', 'country', 'phone_number', 'sex', 'address')

class AuthenticatedProfileSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(many=False, read_only=False)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if validated_data.get('avatar'):
            instance.avatar = validated_data.get('avatar')
        instance.profile.birth = dict(validated_data.get('profile'))['birth'] or instance.profile.country
        instance.profile.is_alumni = dict(validated_data.get('profile'))['is_alumni'] or instance.profile.country
        instance.profile.country = dict(validated_data.get('profile'))['country'] or instance.profile.country
        instance.profile.phone_number = dict(validated_data.get('profile'))['phone_number'] or instance.profile.phone_number
        instance.profile.sex = dict(validated_data.get('profile'))['sex'] or instance.profile.sex
        instance.profile.address = dict(validated_data.get('profile'))['address'] or instance.profile.address
        instance.profile.save()
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'profile',)
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

