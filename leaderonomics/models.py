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
                is_active = True,
                is_staff = True,
            )
            user.save(using=self._db)
        else:
            user = self.model(
                email=UserManager.normalize_email(email),
                username = kwargs['username'] or None,
                avatar = kwargs['avatar'],
                is_active = True,
                is_staff = True,
            )
            profile = Profile.objects.create(birth=kwargs['birth'], is_alumni=kwargs['is_alumni'])
            profile.save(using=self._db)
            user.profile = profile
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
        user.save(using=self._db)
        return user


class Profile(models.Model):
    birth = models.DateField(blank=True, null=True)
    is_alumni = models.BooleanField(default=False)
    country = models.CharField(choices=COUNTRY, default='NL', max_length=256)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)
    sex = models.CharField(choices=SEX, max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)


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
    avatar = models.ImageField(upload_to=uploads.get_avatar_upload_path,
                               blank=True, null=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True)
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


class SocialAccount(models.Model):
    provider = models.CharField(max_length=64)
    uid = models.CharField(max_length=256)
    user = models.ForeignKey(User, related_name='social_accounts', null=True, blank=True)

    def __unicode__(self):
        return "{provider} - {uid}".format(provider=self.provider, uid=self.uid)

    class Meta:
        unique_together = ('provider', 'uid')


class SiteSettings(SingletonModel):
    """
    Singleton model for global settings storage.
    """

    # Facebook settings
    # Actually 16
    facebook_app_id = models.CharField(max_length=128, null=True, blank=True)
    # Actually 32
    facebook_app_secret = models.CharField(max_length=128, null=True, blank=True)

    # Social Links
    facebook_social_link = models.CharField(max_length=256, blank=True, null=True)
    contact_email = models.CharField(max_length=256, blank=True, null=True)

    printer_email = models.EmailField(blank=True, null=True)

    def __unicode__(self):
        return u'Site configuration'

    class Meta:
        verbose_name = "Site Settings"


class Article(models.Model):
    image = models.ImageField(upload_to=uploads.get_article_upload_path,
                              blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    text_highlights = models.TextField(blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, default=list)

    def __str__(self):  # __unicode__ on Python 2
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    file = models.FileField(
        upload_to=uploads.get_video_upload_path,
        blank=True,
        null=True
    )

    def __str__(self):  # __unicode__ on Python 2
        return self.title


class Podcast(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(
        upload_to=uploads.get_podcast_upload_path,
        blank=True,
        null=True
    )

    def __str__(self):  # __unicode__ on Python 2
        return self.title
