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
        exclude = ('last_login', 'password')


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['passport_number'].required = True

    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'passport_number', 'email', 'password')


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

