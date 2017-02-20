from django.contrib.auth.models import User
from django.contrib.auth.views import password_change
from django.contrib.auth import forms as auth_forms, login as auth_login
from django.shortcuts import get_object_or_404, render, resolve_url
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from leaderonomics import settings
from leaderonomics.permissions import IsOwnerOrReadOnly
from leaderonomics.models import Articles, User
from leaderonomics.serializers import *
from leaderonomics.forms import UserForm


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


class Profiles(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AuthenticatedProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


class ArticlesList(generics.ListAPIView):
    queryset = Articles.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = AuthenticatedArticlesSerializer
        else:
            serializer_class = ArticlesSerializer
        return serializer_class


class ArticlesDetail(generics.RetrieveAPIView):
    queryset = Articles.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    
    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = AuthenticatedArticlesSerializer
        return serializer_class



class VideosList(generics.ListAPIView):
    queryset = Videos.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = AuthenticatedVideosSerializer
        else:
            serializer_class = VideosSerializer
        return serializer_class


class VideosDetail(generics.RetrieveAPIView):
    queryset = Videos.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    
    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = AuthenticatedVideosSerializer
        return serializer_class



class PodcastsList(generics.ListAPIView):
    queryset = Podcasts.objects.all()
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

    queryset = Podcasts.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
