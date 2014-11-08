# coding: utf-8

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase

from email_confirm_la.models import EmailConfirmation

# from .utils import get_user_model
# user_model_class = get_user_model()


class BaseTestCase(TestCase):
    # urls = 'test_project.test_project.urls'
    urls = 'email_confirm_la.tests.urls'


class ModelTest(BaseTestCase):
    pass


class ManagerTest(BaseTestCase):

    def setUp(self):
        self.user_obj = User.objects.create_user(username='kiko_mizuhara')
        self.user_email = 'kiko.mizuhara@gmail.com'

    def test_set_email_for_object_for_user_model(self):
        confirmation = EmailConfirmation.objects.set_email_for_object(
            email=self.user_email,
            content_object=self.user_obj,
        )

        self.assertEqual(confirmation.content_object, self.user_obj)
        self.assertEqual(confirmation.email, self.user_email)
        self.assertEqual(confirmation.email_field_name, 'email')
        self.assertTrue(confirmation.is_primary)
        self.assertFalse(confirmation.is_verified)

        mail_obj = mail.outbox[0]
        self.assertIn(confirmation.confirmation_key, mail_obj.body)
        self.assertIn(self.user_email, mail_obj.body)

    def test_set_email_for_object_for_some_model(self):
        pass


class TemplateTest(BaseTestCase):
    pass
