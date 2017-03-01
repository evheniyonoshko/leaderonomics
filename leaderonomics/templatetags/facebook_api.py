# -*- coding: utf-8 -*-

from django.template import Library
from django.template.loader import get_template
# from allauth.socialaccount.models import SocialApp
from leaderonomics.models import SiteSettings

__author__ = 'Yevhenii Onoshko'


register = Library()


@register.simple_tag
def facebook_api():
    context = {'facebook_app_id': SiteSettings.objects.get().facebook_app_id}
    # context = {'facebook_app_id': SocialApp.objects.get(provider='facebook').client_id}
    template = get_template('snippets/facebook_api.html').render(context)
    return template
