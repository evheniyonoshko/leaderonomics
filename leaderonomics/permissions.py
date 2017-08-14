# -*- coding: utf-8 -*-

from rest_framework import permissions

from leaderonomics.models import User

__author__ = 'Yevhenii Onoshko'

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # Write permissions are only allowed to the owner of the profile.
        return obj == request.user
