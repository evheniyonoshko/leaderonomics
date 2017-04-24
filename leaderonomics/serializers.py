from django.contrib.auth.models import User
from rest_framework import serializers
from leaderonomics.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class AuthenticatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'passport_number', 'balance')
        read_only_fields = ('id', 'balance')
