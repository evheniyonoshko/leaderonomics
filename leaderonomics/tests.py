# -*- coding: utf-8 -*-

import json

from django.test import TestCase, Client
from django.core import serializers
from django.core.urlresolvers import reverse

from rest_framework import status

from leaderonomics.models import User

__author__ = 'Yevhenii Onoshko'


class AccountTests(TestCase):
    url_login = reverse('rest_framework:login')
    url_pending = reverse('pending_accounts')
    url_delete = reverse('closed_accounts')
    url_signin = reverse('singin')
    superuser_data = {
        'email': 'admin@example.com',
        'password': 'admin'
    }
    post_data = {
        'email': 'test@test.com',
        'password': 'test_password',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'passport_number': 'TT123321'
    }
    def test_create_superuser(self):
        """
        Ensure we can create a new superuser account.
        """
        User.objects.create_superuser(**self.superuser_data)
        self.assertEqual(User.objects.get().email, 'admin@example.com')

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('singin')
        data = self.post_data
        self.client = Client(enforce_csrf_checks=True)
        signin = self.client.get(self.url_signin)
        csrftoken = signin.cookies['csrftoken']
        data['csrfmiddlewaretoken']=csrftoken.value
        response = self.client.post(self.url_signin, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@test.com')

    def test_login(self):
        """
        Ensure we can login with email and password.
        """
        data = self.superuser_data
        User.objects.create_superuser(**data)
        client_logged = self.client.login(**data)
        self.assertEqual(client_logged, True)
        signin = self.client.get(self.url_login)
        csrftoken = signin.cookies['csrftoken']
        data['csrfmiddlewaretoken']=csrftoken.value
        response = self.client.post(self.url_login, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_pending_accounts(self):
        """
        Ensure we can change existing account object.
        """
        User.objects.create_superuser(**self.superuser_data)
        signin = self.client.get(self.url_signin)
        csrftoken = signin.cookies['csrftoken']
        self.post_data['csrfmiddlewaretoken']=csrftoken.value
        self.client.post(self.url_signin, self.post_data, format='json')
        self.client.login(**self.superuser_data)
        response = self.client.get(self.url_pending)
        self.assertEqual(self.post_data['email'], response.data[0]['email'])
        account_id = response.data[0]['id']
        data = {'id': response.data[0]['id'],
                'email': response.data[0]['email'],
                'first_name': response.data[0]['first_name'],
                'last_name': response.data[0]['last_name'],
                'is_active': True}
        url = self.url_pending + '{}/'.format(account_id) 
        response = self.client.patch(url,
                                     json.dumps(data),
                                     'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('is_active'), True)

    def test_delete_accounts(self):
        """
        Ensure we can change existing account object.
        """
        User.objects.create_superuser(**self.superuser_data)
        signin = self.client.get(self.url_signin)
        csrftoken = signin.cookies['csrftoken']
        self.post_data['csrfmiddlewaretoken']=csrftoken.value
        self.client.post(self.url_signin, self.post_data, format='json')
        self.client.login(**self.superuser_data)
        response = self.client.get(self.url_delete)
        if response.data:
            self.assertEqual(self.post_data['email'], response.data[0]['email'])
            account_id = response.data[0]['id']
            url = self.url_delete + '{}/'.format(account_id)
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            response = self.client.delete(reverse('account_delete'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(self.post_data['email'], response.data[0]['email'])
            account_id = response.data[0]['id']
            url = self.url_delete + '{}/'.format(account_id)
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
