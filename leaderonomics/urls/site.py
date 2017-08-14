# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from rest_framework.authtoken.views import obtain_auth_token

from leaderonomics.views.views import *

__author__ = 'Yevhenii Onoshko'

urlpatterns = [
    url(r'^$', base),
    url(r'^admin/', include('leaderonomics.urls.admin')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                                namespace='rest_framework')),
    url(r'^api-auth/singin/', Singin.as_view(), name='singin'),

]

urlpatterns += [
    url(r'^api/v1.0/accounts/pending/$', PendingMenegersView.as_view(), name='pending_accounts'),
    url(r'^api/v1.0/accounts/pending/(?P<pk>[0-9]+)/$', PendingMenegersDatailView.as_view()),
    url(r'^api/v1.0/accounts/closed/$', CloseAccountView.as_view(), name='closed_accounts'),
    url(r'^api/v1.0/accounts/closed/(?P<pk>[0-9]+)/$', CloseAccountDatailView.as_view()),
    url(r'^api/v1.0/accounts/client/profile/$', UserView.as_view()),
    url(r'^api/v1.0/accounts/client/change_password/', my_password_change, name='change_password'),
    url(r'^api/v1.0/accounts/client/delete/', account_delete, name='account_delete'),
]
