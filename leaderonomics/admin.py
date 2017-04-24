# -*- coding: utf-8 -*-

import csv
from io import StringIO

from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from sorl.thumbnail.admin import AdminImageMixin

from leaderonomics.forms import UserAdminForm
from leaderonomics.models import User


def download_csv(modeladmin, request, queryset):
    f = StringIO()
    writer = csv.writer(f)
    writer.writerow(['id', 'username', 'email', 'first_name', 'last_name', 'last_login',
                     'registered', 'password', 'is_active',
                     'is_staff', 'is_superuser'])

    for s in queryset.order_by('id'):
        writer.writerow([s.id, s.username, s.email, s.first_name, s.last_name, s.last_login,
                         s.registered, s.password, s.is_active,
                         s.is_staff, s.is_superuser])
    f.seek(0)
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=leaderonomics-user-info.csv'
    return response

download_csv.short_description = "Export to csv"

class UserAdmin(BaseUserAdmin):
    form = UserAdminForm
    ordering = ('registered',)
    list_filter = ['is_active', 'is_closed']

    list_display = (
        'email', 'first_name', 'last_name', 'passport_number', 'is_superuser', 'is_active', 'is_staff', 'is_closed'
    )

    fieldsets = (
        ('Info', {
            'fields': ('email', 'first_name', 'last_name', 'passport_number')
        }),
        ('Permissions', {
            'fields': ('is_superuser','is_staff', 'is_active', 'is_closed')
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username',
                       'first_name', 'last_name', 'passport_number')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff', 'is_active', 'is_closed')
        }),
    )
    actions = [download_csv,]

    class Media:
        css = {
            # 'all': (
            #     'css/select2.min.css',
            #     'css/bootstrap.min.css',
            # )
        }
        js = (
            # 'js/jquery-3.1.0.min.js',
            # 'js/bootstrap.min.js',
            # 'js/select2.full.min.js',
            # 'js/select2.full.min.js',
            # 'js/js.cookie.js',
        )


admin.site.register(User, UserAdmin)
