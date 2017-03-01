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
from leaderonomics.social.config import CONFIG as SOCIAL_CONFIG


@login_required
def welcome(request):
    """
    Renders Welcome message

    :param request: django.http.request.HttpRequest
    :return: django.http.response.HttpResponse
    """
    return render(request, 'snippets/login_success.html')


# Social auth views
def social_login(request, provider):
    """
    Get OAuth provider name from GET params and generates authorization URL for current request

    :param request: django.http.request.HttpRequest
    :param provider: str
    :return: django.http.response.HttpResponseRedirect
    """
    request.session['next_path'] = request.GET.get('next')
    config = SOCIAL_CONFIG[provider]

    if provider == 'facebook':
        session = OAuth2Session(
            config['client_id'],
            redirect_uri=reverse('social_callback', args=(provider,)),
            scope=['public_profile', 'email', 'user_friends']
        )
        session = facebook_compliance_fix(session)
    else:
        session = OAuth2Session(
            config['client_id'],
            redirect_uri=reverse('social_callback', args=(provider,)),
            scope=config['scope'])
    authorisation_url, state = session.authorization_url(config['authorization_base_url'])

    request.session['oauth_provider'] = provider
    request.session['oauth_state'] = state
    return redirect(authorisation_url)


def social_login_callback(request, provider):
    """
    Callback view for OAuth login.
    Extracts auth token from request and passes it to current session

    :param request: django.http.request.HttpRequest
    :param provider: str
    :return: django.http.response.HttpResponse
    """
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    config = SOCIAL_CONFIG[provider]
    # import ipdb; ipdb.set_trace()
    session = OAuth2Session(config['client_id'],
                            state=request.session.pop('oauth_state'),
                            redirect_uri=reverse('social_callback', args=(provider, )))
    print(request.get_full_path())
    
    token = session.fetch_token(config['token_url'],
                                client_secret=config['client_secret'],
                                authorization_response=request.get_full_path())

    request.session['oauth_token'] = token
    return redirect('social_final')


def social_login_final(request):
    """
    Takes auth login from current session,
    loads user information from provider,
    finds/create User with email taken from provider and logs he/she in.

    :param request: django.http.request.HttpRequest
    :return: django.http.response.HttpResponse
    """

    is_new_user = False

    config = SOCIAL_CONFIG[request.session['oauth_provider']]
    print(request.session['oauth_token'])
    session = OAuth2Session(config['client_id'], token=request.session['oauth_token'])
    userinfo = ''

    if request.session['oauth_provider'] == 'facebook':
        userinfo = session.get('https://graph.facebook.com/me?fields=id,name,email,picture')

    parsed_userinfo = json.loads(userinfo.content)

    print(type(parsed_userinfo))
    print(type(parsed_userinfo['picture']))
    print(parsed_userinfo)

    try:
        account = SocialAccount.objects.get(uid=parsed_userinfo['id'])
    except SocialAccount.DoesNotExist:
        account = SocialAccount(
            provider=request.session['oauth_provider'],
            uid=parsed_userinfo['id']
        )
        account.save()

    try:
        user = User.objects.get(email=parsed_userinfo['email'])
    except User.DoesNotExist:
        if account.provider == 'facebook':
            if parsed_userinfo.get('email', None):
                user = User(email=parsed_userinfo['email'])
            else:
                user = User(email=account.uid + "@facebook.com")
        else:
            user = User(email=parsed_userinfo['email'])
        user.is_active = True
        user.save()
        is_new_user = True

    if user:
        try:
            user.social_accounts.get(provider__exact=account.provider, uid__exact=account.uid)
        except SocialAccount.DoesNotExist:
            account.user = user
            account.save()
            print(user.social_accounts.all())
        else:
            print('Find')

        finally:
            if account.provider == 'facebook':
                if not user.avatar:
                    user.avatar_url = parsed_userinfo['picture']['data']['url']
                if not user.first_name:
                    user.first_name = parsed_userinfo['name'].split()[0]
                if not user.last_name:
                    user.last_name = parsed_userinfo['name'].split()[-1]
            else:
                if not user.avatar:
                    user.avatar_url = parsed_userinfo['picture']
                if not user.first_name:
                    user.first_name = parsed_userinfo['given_name']
                if not user.last_name:
                    user.last_name = parsed_userinfo['family_name']
            user.save()
            if is_new_user:
                new_password = generate_pass(12)
                user.set_password(new_password)
                user.save()
                email_subject = render_to_string('email/social_welcome_subject.txt', context=None)
                email_body = render_to_string(
                    'email/social_welcome_email.txt',
                    context={
                        'name': user.first_name,
                        'surname': user.last_name,
                        'email': user.email,
                        'password': new_password
                    }
                )
                send_mail(
                    email_subject,
                    email_body,
                    SiteSettings.objects.get().contact_email,
                    (user.email, )
                )
        print(user.social_accounts.all())

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, user)
    print(user)
    next_path = request.session.pop('next_path', None)
    if next_path:
        return redirect(next_path)
    return redirect('index')


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
