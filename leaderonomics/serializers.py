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
        fields = ('birth', 'country', 'phone_number', 'sex', 'address', 'is_alumni')

class AuthenticatedProfileSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(many=False, read_only=False)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if validated_data.get('avatar'):
            instance.avatar = validated_data.get('avatar')
        if instance.profile_id:
            instance.profile.birth = dict(validated_data.get('profile'))['birth'] or instance.profile.birth or None
            instance.profile.is_alumni = dict(validated_data.get('profile'))['is_alumni'] or instance.profile.is_alumni or None
            instance.profile.country = dict(validated_data.get('profile'))['country'] or instance.profile.country or None
            instance.profile.phone_number = dict(validated_data.get('profile'))['phone_number'] or instance.profile.phone_number or None
            instance.profile.sex = dict(validated_data.get('profile'))['sex'] or instance.profile.sex or None
            instance.profile.address = dict(validated_data.get('profile'))['address'] or instance.profile.address or None
            instance.profile.save()
            instance.save()
        else:
            profile = Profile.objects.create(birth=dict(validated_data.get('profile'))['birth'] or None,
                                             is_alumni=dict(validated_data.get('profile'))['is_alumni'] or None,
                                             country=dict(validated_data.get('profile'))['country'] or None,
                                             phone_number=dict(validated_data.get('profile'))['phone_number'] or None,
                                             sex=dict(validated_data.get('profile'))['sex'] or None,
                                             address=dict(validated_data.get('profile'))['address'] or None)
        instance.profile = profile
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'profile',)
        read_only_fields = ('id',)


class ArticlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        exclude = ('id',)
        read_only_fields = ('title', 'text')


class AuthenticatedArticlesSerializer(ArticlesSerializer):
    class Meta:
        model = Article
        read_only_fields = ('id', 'title', 'text')


class VideosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        exclude = ('id',)
        read_only_fields = ('title', 'description', 'file')


class AuthenticatedVideosSerializer(ArticlesSerializer):
    class Meta:
        model = Video
        read_only_fields = ('id', 'title', 'description', 'file')


class PodcastsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Podcast
        exclude = ('id',)
        read_only_fields = ('title', 'file')


class AuthenticatedPodcastsSerializer(ArticlesSerializer):
    class Meta:
        model = Podcast
        read_only_fields = ('id', 'title', 'file')

