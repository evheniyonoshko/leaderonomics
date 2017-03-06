# -*- coding: utf-8 -*-

from leaderonomics.models import SiteSettings

__author__ = 'Yevhenii Onoshko'

settings = SiteSettings.objects.get()


CONFIG = {
    'facebook': {
        'client_id': settings.facebook_app_id,
        'client_secret': settings.facebook_app_secret,
        'authorization_base_url': 'https://www.facebook.com/dialog/oauth',
        'token_url': 'https://graph.facebook.com/oauth/access_token',
        # 'redirect_uri': reverse('social_callback', args='facebook'),
    },
}