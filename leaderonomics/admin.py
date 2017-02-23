# -*- coding: utf-8 -*-

import csv
from io import StringIO

from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from sorl.thumbnail.admin import AdminImageMixin

from leaderonomics.forms import UserAdminForm
from leaderonomics.models import *


def download_csv(modeladmin, request, queryset):
    f = StringIO()
    writer = csv.writer(f)
    writer.writerow(['id', 'username', 'email', 'first_name', 'last_name', 'last_login',
                     'avatar_url', 'registered', 'avatar', 'password', 'is_active',
                     'is_staff', 'is_superuser'])

    for s in queryset.order_by('id'):
        writer.writerow([s.id, s.username, s.email, s.first_name, s.last_name, s.last_login,
                         s.avatar_url, s.registered, s.avatar, s.password, s.is_active,
                         s.is_staff, s.is_superuser])
    f.seek(0)
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=leaderonomics-user-info.csv'
    return response

download_csv.short_description = "Export to csv"

class UserAdmin(AdminImageMixin, BaseUserAdmin):
    form = UserAdminForm

    list_filter = []

    list_display = (
        'email', 'is_superuser', 'is_active', 'is_staff'
    )

    fieldsets = (
        ('Info', {
            'fields': ('avatar', 'email', 'first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('user_permissions', 'groups', 'is_superuser',
                       'is_staff', 'is_active')
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username',
                       'first_name', 'last_name', 'birth', 'is_alumni', 'avatar')
        }),
        ('Permissions', {
            'fields': ('user_permissions', 'groups',
                       'is_superuser', 'is_staff', 'is_active')
        }),
    )
    actions = [download_csv,]

    class Media:
        css = {
            'all': (
                'css/select2.min.css',
                'css/bootstrap.min.css',
            )
        }
        js = (
            'js/jquery-3.1.0.min.js',
            'js/bootstrap.min.js',
            # 'js/select2.full.min.js',
            'js/select2.full.min.js',
            'js/js.cookie.js',
        )


class ArticleAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('title', 'text', 'image', 'text_highlights', 'tags')
    search_fields = ('title', )
    fields = ('title', 'text', 'image', 'text_highlights', 'tags')


class VideoAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('title', 'description')
    search_fields = ('title', )
    fields = ('title', 'description', 'file')


class PodcastAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('title',)
    search_fields = ('title', )
    fields = ('title', 'file')


admin.site.register(User, UserAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Podcast, PodcastAdmin)
