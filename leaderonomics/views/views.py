# -*- coding: utf-8 -*-
import os
import json
from django.contrib.auth.views import password_change
from django.contrib import auth
from django.contrib.auth import forms as auth_forms, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django import forms
from django.urls import reverse
from rest_framework import generics, permissions
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

from leaderonomics import settings
from leaderonomics.models import *
from leaderonomics.tools.password_generator import generate_pass
from leaderonomics.permissions import IsOwnerOrReadOnly
from leaderonomics.serializers import *
from leaderonomics.forms import UserForm


@login_required
def welcome(request):
    """
    Renders Welcome message

    :param request: django.http.request.HttpRequest
    :return: django.http.response.HttpResponse
    """
    return render(request, 'snippets/login_success.html')


def my_password_change(request):
    ''' Change pasword method '''
    return password_change(request,
                           post_change_redirect=request.path,
                           template_name='rest_framework/change_password.html')


class Singin(FormView):
    template_name = 'rest_framework/singin.html'
    def post(self, request):
        data = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'username': request.POST.get('username') or None,
            'is_alumni': True if request.POST.get('is_alumni') == 'on' else False,
            'avatar': request.FILES.get('avatar') or None
        }
        birth_year = request.POST.get('birth_year')
        birth_month = request.POST.get('birth_month')
        birth_day = request.POST.get('birth_day')
        if birth_year and birth_month and birth_day:
            data['birth'] = birth_year + '-' + birth_month + '-' + birth_day
        else:
            data['birth'] = None
        form = UserForm(data)
        if form.is_valid():
            try:
                user = User.objects.get(email=data['email'])
            except:
                user = User.objects.create_user(**data)
                return HttpResponseRedirect(resolve_url(settings.SINGIN_REDIRECT_URL))
        else:
            print('INVALID')
            form = UserForm(data)
            context = self.get_context_data(**{
                'form': form
            })
            return self.render_to_response(context)
        form = UserForm(request.GET)
        context = self.get_context_data(**{
            'form': form
        })
        return self.render_to_response(context)

    def get(self, request):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        singin_form = UserForm(request.GET)
        return self.form_invalid(singin_form)


class Profile(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AuthenticatedProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)



class ArticlesList(generics.ListAPIView):
    queryset = Article.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = AuthenticatedArticlesSerializer
        else:
            serializer_class = ArticlesSerializer
        return serializer_class


class ArticlesDetail(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    
    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = AuthenticatedArticlesSerializer
        return serializer_class



class VideosList(generics.ListAPIView):
    queryset = Video.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = AuthenticatedVideosSerializer
        else:
            serializer_class = VideosSerializer
        return serializer_class


class VideosDetail(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    
    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = AuthenticatedVideosSerializer
        return serializer_class



class PodcastsList(generics.ListAPIView):
    queryset = Podcast.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = AuthenticatedPodcastsSerializer
        else:
            serializer_class = PodcastsSerializer
        return serializer_class


class PodcastsDetail(generics.RetrieveAPIView):
    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = AuthenticatedPodcastsSerializer
        return serializer_class

    queryset = Podcast.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
