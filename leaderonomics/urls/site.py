# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', include('leaderonomics.urls.admin')),
    url(r'^admin_tools/', include('admin_tools.urls')),
]

