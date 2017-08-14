# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import models as auth_models
from django.contrib.postgres.fields import ArrayField

from sorl.thumbnail import ImageField
from solo.models import SingletonModel

from leaderonomics.tools import uploads

from lib import country_list

__author__ = 'Yevhenii Onoshko'

COUNTRY = list(country_list.generate_country_list())
SEX = [('Male', 'Male'), ('Female', 'Female')]


class UserManager(auth_models.BaseUserManager):
    """
    Custom User Manager. Needed for Django auth to work with custom User model
    """
    def create_user(self, email, password, is_super=False, **kwargs):
        """
        Creates and saves User
        """
        if not email:
            raise ValueError('Users must have an email address')
        if is_super:
            user = self.model(
                email=UserManager.normalize_email(email),
            )
            user.save(using=self._db)
        else:
            user = self.model(
                email=UserManager.normalize_email(email),
                first_name = kwargs['first_name'] or None,
                last_name = kwargs['last_name'] or None,
                passport_number = kwargs['passport_number'] or None,
            )
            user.save(using=self._db)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password):
        """
        Creates and saves superuser
        """
        user = self.create_user(email=email, password=password, is_super=True )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
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
    passport_number = models.CharField(max_length=8, blank=True)
    balance = models.FloatField(default=0.00)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.get_full_name()


    def __str__(self):
        return self.get_full_name()


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
