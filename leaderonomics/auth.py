from leaderonomics import models
from django.contrib.auth import get_user_model


class EmailBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return models.User.objects.get(pk=user_id)
        except:
            return None
