# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from leaderonomics.views.views import *
from rest_framework.authtoken.views import obtain_auth_token

# Testing of rest-auth with social media
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

urlpatterns = [
    url(r'^admin/', include('leaderonomics.urls.admin')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                                namespace='rest_framework')),
    url(r'^api-auth/singin/', Singin.as_view(), name='singin'),
    url(r'^accounts/', include('allauth.urls')),
    # Social auth
    url(r'^social/login/final/$', social_login_final, name='social_final'),
    url(r'^social/login/(\w*)/$', social_login, name='social_login'),
    url(r'^social/login/(\w*)/callback$', social_login_callback, name='social_callback'),

    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='facebook_login'),
    url(r'^welcome/$', welcome, name='welcome'),
]

urlpatterns += [
    url(r'^api/articles/$', ArticlesList.as_view()),
    url(r'^api/articles/(?P<pk>[0-9]+)/$', ArticlesDetail.as_view()),
    url(r'^api/videos/$', VideosList.as_view()),
    url(r'^api/videos/(?P<pk>[0-9]+)/$', VideosDetail.as_view()),
    url(r'^api/podcasts/$', PodcastsList.as_view()),
    url(r'^api/podcasts/(?P<pk>[0-9]+)/$', PodcastsDetail.as_view()),
    url(r'^user/profile/(?P<pk>[0-9]+)/$', Profile.as_view()),
]

urlpatterns += [
    url(r'^accounts/change_password/', my_password_change, name='change_password'),
]
