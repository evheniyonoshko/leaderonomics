from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from sorl.thumbnail.admin import AdminImageMixin
from leaderonomics.forms import UserAdminForm
from leaderonomics.models import User


class UserAdmin(AdminImageMixin, BaseUserAdmin):
    form = UserAdminForm

    list_filter = []

    list_display = (
        'email',
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
            'fields': ('email', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('user_permissions', 'groups',
                       'is_superuser', 'is_staff', 'is_active')
        })
    )

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

admin.site.register(User, UserAdmin)
