# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from leaderonomics.views import admin as admin_views


__author__ = 'Yevhenii Onoshko'

urlpatterns = [
    url(r'', include(admin.site.urls)),
]
