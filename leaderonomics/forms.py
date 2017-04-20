# -*- coding: utf-8 -*-
import datetime
from django import forms
from leaderonomics.models import User
from leaderonomics import settings

__author__ = 'Yevhenii Onoshko'


class UserAdminForm(forms.ModelForm):
    user_permissions = forms.SelectMultiple(
        attrs={
            'class': 'select2'
        }
    )

    class Meta:
        model = User
        exclude = ('last_login', 'password', 'avatar_url')

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        year_choices = (year for year in range(1940, datetime.date.today().year + 1))
        self.fields['birth'].widget = forms.SelectDateWidget(years=year_choices)
    birth = forms.DateField(required=False)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    is_alumni = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'avatar')

class LoginForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(
        label='E-Mail',
        max_length=128,
        widget=forms.TextInput(attrs={'placeholder': 'tinyperson@gmail'})
    )
    password = forms.CharField(
        label='password',
        max_length=128,
        widget=forms.PasswordInput(attrs={'placeholder': 'password'})
    )

class AllauthLoginForm(LoginForm):
    """
    Customized form for use with allauth
    """
    def __init__(self, *args, **kwargs):
        super(AllauthLoginForm, self).__init__()
        self.fields['login'] = self.fields['email']
