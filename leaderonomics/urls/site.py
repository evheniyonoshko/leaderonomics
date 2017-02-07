# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from leaderonomics.views.views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^admin/', include('leaderonomics.urls.admin')),
    url(r'^admin_tools/', include('admin_tools.urls')),
]

urlpatterns += [
    url(r'^api/articles/$', ArticlesList.as_view()),
    url(r'^api/articles/(?P<pk>[0-9]+)/$', ArticlesDetail.as_view()),
    # url(r'^api/users/$', views.UserList.as_view()),
    # url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns += [
    url(r'^api-token-auth/', include('rest_framework.urls',
                             namespace='rest_framework')),
]
