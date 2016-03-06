# coding: utf-8

from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite

from model_mommy import mommy

from .base import BaseTestCase
from email_confirm_la.models import EmailConfirmation


class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


class AdminTest(BaseTestCase):

    def setUp(self):
        mommy.make(
            'email_confirm_la.EmailConfirmation',
            _quantity=1,
        )
        self.site = AdminSite()

    def test_confirm_email(self):
        ecla_admin = ModelAdmin(EmailConfirmation, self.site)
        ecla_form = ecla_admin.get_form(request)

        self.assertIn('email_field_name', ecla_form.base_fields.keys())
        self.assertIn('email', ecla_form.base_fields.keys())
