from rest_framework import permissions
from leaderonomics.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_staff:
            return True
        print(request.user.is_staff)
        # Write permissions are only allowed to the owner of the profile.
        import ipdb; ipdb.set_trace()
        return obj == request.user
