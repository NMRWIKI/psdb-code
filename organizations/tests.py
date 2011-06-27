"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from organizations import models 

class UrlTests(TestCase):

    def setUp(self):
        self.client = Client() 

    def test_org_main(self):
        response = self.client.get(reverse('org_main'))
        self.assertEquals(response.status_code, 200)

    def test_org_creation_post(self):
        response = self.client.post(
                    reverse('create_lab'),
                    {
                        'org_type': '8',
                    })
        self.assertEquals(response.status_code, 200)

    def test_org_creation_get(self):
        response = self.client.get(reverse('create_lab'))
        self.assertEquals(response.status_code, 200)

class LoggedInUrlTests(UrlTests):
    def setUp(self):
        super(LoggedInUrlTests, self).setUp()
        self.user = User.objects.create_user(
                                        'john',
                                        'lennon@thebeatles.com',
                                        'johnpassword'
                                    )
        self.client.login(username = 'john', password = 'johnpassword')
