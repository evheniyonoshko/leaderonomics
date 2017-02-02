# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth import models as auth_models
from sorl.thumbnail import ImageField
from leaderonomics.tools import uploads

__author__ = 'Yevhenii Onoshko'


class UserManager(auth_models.BaseUserManager):
    """
    Custom User Manager. Needed for Django auth to work with custom User model
    """
    def create_user(self, email, password=None):
        """
        Creates and saves User
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=UserManager.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves superuser
        """
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(auth_models.PermissionsMixin, auth_models.AbstractBaseUser):
    """
    Custom User Model. Use email as username.
    Needed to override default Django User which use username as username :)

    """
    registered = models.DateField(auto_now_add=True)
    email = models.EmailField(max_length=128, unique=True)
    username = models.CharField(max_length=128, blank=True, null=True)
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    avatar = ImageField(upload_to=uploads.get_avatar_upload_path,
                        blank=True, null=True)
    avatar_url = models.URLField(default='http://www.gravatar.com/avatar/?d=mm&s=200')
    is_active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.get_full_name()

    # def __unicode__(self):
    #     return self.get_full_name()

    def __str__(self):
        return self.get_full_name()

    # def has_perm(self, perm, obj=None):
    #     return True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(User, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def has_module_perms(self, app_label):
        return True


class Articles(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(blank=True, null=True)


class Videos(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    file = models.FileField(
        upload_to=uploads.get_video_upload_path,
        blank=True,
        null=True
    )


class Podcasts(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(
        upload_to=uploads.get_podcast_upload_path,
        blank=True,
        null=True
    )
