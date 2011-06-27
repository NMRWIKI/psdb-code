"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from organizations import models, forms

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
                        'org_type': 'fish',
                    })
        self.assertEquals(response.status_code, 302)

    def test_org_creation_get(self):
        response = self.client.get(reverse('create_lab'))
        self.assertEquals(response.status_code, 302)

class LoggedInUrlTests(UrlTests):
    def setUp(self):
        super(LoggedInUrlTests, self).setUp()
        self.user = User.objects.create_user(
                                        'john',
                                        'lennon@thebeatles.com',
                                        'johnpassword'
                                    )
        self.client.login(username = 'john', password = 'johnpassword')

    def test_org_creation_post(self):
        response = self.client.post(reverse('create_lab'))
        self.assertEquals(response.status_code, 200)

    def test_org_creation_get(self):
        response = self.client.post(reverse('create_lab'))
        self.assertEquals(response.status_code, 200)

class OrganizationFormTests(TestCase):
    def test_invalid_org_type_fails(self):
        data = {
            'org_type': 55,
            'name': 'asdffasfsafsa',
            'description': 'wqwgwfwfffadfasfsaf',
            'url': 'http://youtube.com'
        }
        form = forms.OrganizationForm(data)
        self.assertEquals(form.is_valid(), False, 'form is invalid')
        self.assertTrue('org_type' in form._errors, 'org id is invalid')
        organization = models.Organization.objects.get(id = 1)
        response = self.client.get(organization.get_absolute_url())
        self.assertEquals(response.status_code, 200)

  #  def test_valid_form_creates_org(self):       
 #       data = {
 #           'org_type': 2,
 #           'name': 'asdffasfsafsa',
 #           'description': 'wqwgwfwfffadfasfsaf',
 #           'url': 'http://youtube.com'
 #       }
 #       form = forms.OrganizationForm(data)
 #       self.assertEquals(form.is_valid(), True)
 #       self.client.post(reverse('create_lab', form)
 #       organization = models.Organization.objects.get(id = 1)
 #       response = self.client.get(organization.get_absolute_url())
 #       self.assertEquals(response.status_code, 200)
