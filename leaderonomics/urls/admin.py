# -*- coding: utf-8 -*-

from leaderonomics.views import admin as admin_views
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

__author__ = 'Yevhenii Onoshko'

urlpatterns = [
    url(r'', include(admin.site.urls)),
]
