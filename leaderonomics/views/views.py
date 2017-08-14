# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.views import password_change
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.core.mail import send_mail

from rest_framework import generics, permissions

from leaderonomics.settings import SINGIN_REDIRECT_URL
from leaderonomics.models import User
from leaderonomics.permissions import IsOwnerOrReadOnly
from leaderonomics.serializers import PendingMenegersSerializer, CloseAccountsSerializer, \
                                      UserSerializer, AuthenticatedUserSerializer
from leaderonomics.forms import UserForm


def base(request):
    '''
    Base url, when you get 'http://localhost:8000/' 
    you will redirected to 'http://localhost:8000/api/v1.0/accounts/client/profile/'
    '''
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
    '''
    Singin FormView with GET and POST methods
    '''
    template_name = 'rest_framework/singin.html'

    def post(self, request):
        '''
        POST method for singin view
        '''
        data = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'passport_number': request.POST.get('passport_number'),
        }

        form = UserForm(data)
        if form.is_valid():
            user = get_user_model().objects.create_user(**data)
            menegers = User.objects.filter(is_staff=True)
            meneger_emails = [meneger.email for meneger in menegers]
            send_mail(
                'Account created',
                'You have new accounts that need activate',
                'yevhen.didi@gmail.com',
                meneger_emails,
                fail_silently = False,
            )
            return HttpResponseRedirect(resolve_url(SINGIN_REDIRECT_URL))
        else:
            print('INVALID', form.errors)
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

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        form = UserForm()
        return self.render_to_response(self.get_context_data(form=form))

class UserView(generics.ListAPIView):
    '''
    User list view
    '''
    serializer_class = AuthenticatedUserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return User.objects.filter(id=int(self.request.user.id))


class PendingMenegersView(generics.ListAPIView):
    '''
    List view of pending users
    '''
    queryset = User.objects.filter(is_active=False, is_closed=False)
    serializer_class = PendingMenegersSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


class PendingMenegersDatailView(generics.RetrieveUpdateAPIView):
    '''
    List view of pending user with PUT method for activate user
    '''
    queryset = User.objects.filter(is_active=False, is_closed=False)
    serializer_class = PendingMenegersSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def put(self, request, *args, **kwargs):
        '''
        Overrided put method, delete obj with emain notification
        '''
        obj = User.objects.get(pk=int(kwargs['pk']))
        if request.POST['is_active'] == 'true':
            message = 'Your account was activated'
        else:
            message = 'Your account was deactivated'
        send_mail(
            'Account activate',
            message,
            'yevhen.didi@gmail.com',
            [obj.email],
            fail_silently = False,
        )
        return self.update(request, *args, **kwargs)


class CloseAccountView(generics.ListAPIView):
    '''
    View for account list view
    '''
    queryset = User.objects.filter(is_closed=True)
    serializer_class = CloseAccountsSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


class CloseAccountDatailView(generics.RetrieveDestroyAPIView):
    '''
    View for delete account
    '''
    queryset = User.objects.filter(is_closed=True)
    serializer_class = CloseAccountsSerializer
    permission_classes = permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def delete(self, request, *args, **kwargs):
        '''
        Overrided delete method, delete obj with emain notification
        '''
        obj = User.objects.get(pk=int(kwargs['pk']))
        send_mail(
            'Account delete',
            'Your account was deleted',
            'yevhen.didi@gmail.com',
            [obj.email],
            fail_silently = False,
        )
        return self.destroy(request, *args, **kwargs)
