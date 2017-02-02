# -*- coding: utf-8 -*-

from leaderonomics.views import admin as admin_views
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

__author__ = 'Yevhenii Onoshko'

custom_views = ([
    url(r'^save_csv$', admin_views.save_csv, name='save_csv'),
], 'custom')

urlpatterns = [
    url(r'', include(admin.site.urls)),
    url(r'^custom/', include(custom_views))
]
