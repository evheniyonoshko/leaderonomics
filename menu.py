"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'leaderonomics.menu.CustomMenu'
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
# from django.contrib.staticfiles.templatetags.staticfiles import static
from leaderonomics.models import User

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for ad_folders admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.MenuItem(_('Article'), reverse('admin:leaderonomics_article_changelist')),
            items.MenuItem(_('Video'), reverse('admin:leaderonomics_video_changelist')),
            items.MenuItem(_('Podcast'), reverse('admin:leaderonomics_podcast_changelist')),

        ]
        self.children += [
            items.ModelList(
                _('Users'),
                models=('leaderonomics.models.User', 'django.contrib.auth.*',)
            )
        ]


    class Media:
        css = ()
        js = (
            # 'js/admin/menu.js',
            # 'js/jquery-3.1.0.min.js',
            # 'js/bootstrap.min.js',
            # 'js/select2.full.min.js',
            # 'js/js.cookie.js',
        )


    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)
