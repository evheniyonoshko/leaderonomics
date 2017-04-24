# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.views import password_change
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
# from django.core.mail import send_mail
from rest_framework import generics, permissions

from leaderonomics.settings import SINGIN_REDIRECT_URL
from leaderonomics.models import User
from leaderonomics.permissions import IsOwnerOrReadOnly
from leaderonomics.serializers import PendingMenegersSerializer, CloseAccountsSerializer, \
                                      UserSerializer, AuthenticatedUserSerializer
from leaderonomics.forms import UserForm


def base(request):
    """
    Renders Welcome message

    :param request: django.http.request.HttpRequest
    :return: django.http.response.HttpResponse
    """
    return redirect('/api/v1.0/accounts/client/profile/')

def my_password_change(request):
    ''' Change pasword method '''
    return password_change(request,
                           post_change_redirect=request.path,
                           template_name='rest_framework/change_password.html')

def account_delete(request):
    ''' Account delete method '''
    user = User.objects.get(id=request.user.id)
    user.is_active = False
    user.is_closed = True
    user.save()
    return redirect('/api/v1.0/accounts/client/profile/')



class Singin(FormView):
    template_name = 'rest_framework/singin.html'
    def post(self, request):
        data = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'first_name': request.POST.get('first_name') or None,
            'last_name': request.POST.get('last_name') or None,
            'passport_number': request.POST.get('passport_number') or None,
            'is_staff': True,
        }

        form = UserForm(data)
        if form.is_valid():
            try:
                user = User.objects.get(email=data['email'])
            except:
                user = get_user_model().objects.create_user(**data)
                return HttpResponseRedirect(resolve_url(SINGIN_REDIRECT_URL))
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


class UserView(generics.ListAPIView):
    serializer_class = AuthenticatedUserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return User.objects.filter(id=int(self.request.user.id))


class PendingMenegersView(generics.ListAPIView):
    serializer_class = PendingMenegersSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return User.objects.filter(is_active=False, is_closed=False)

class PendingMenegersDatailView(generics.RetrieveUpdateAPIView):
     queryset = User.objects.filter(is_active=False, is_closed=False)
     permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
     
     def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = PendingMenegersSerializer
            return serializer_class


class CloseAccountView(generics.ListAPIView):
    serializer_class = CloseAccountsSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return User.objects.filter(is_closed=True)

class CloseAccountDatailView(generics.RetrieveDestroyAPIView):
     queryset = User.objects.filter(is_closed=True)
     permission_classes = permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
     
     def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated():
            serializer_class = CloseAccountsSerializer
            return serializer_class

