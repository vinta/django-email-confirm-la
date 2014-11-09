# coding: utf-8

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core import mail
from django.core.management import call_command
from django.utils import timezone

from freezegun import freeze_time
from model_mommy import mommy

from .base import BaseTestCase
from email_confirm_la.exceptions import EmailConfirmationExpired
from email_confirm_la.models import EmailConfirmation
from test_app.models import YourModel


class ManagerTest(BaseTestCase):

    def setUp(self):
        self.user_obj = User.objects.create_user(username='kiko_mizuhara')
        self.user_email = 'kiko.mizuhara@gmail.com'
        self.user_email_2 = 'kiko.mizuhara@yahoo.com'

        self.your_obj = YourModel.objects.create()
        self.your_customer_support_email = 'marvin@therestaurantattheendoftheuniverse.com'
        self.your_marketing_email = 'arthur@therestaurantattheendoftheuniverse.com'

    def test_set_email_for_object_with_user_model(self):
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

        confirmation.confirm()

        self.assertTrue(confirmation.is_verified)
        self.assertEqual(self.user_obj.email, self.user_email)

    def test_set_email_for_object_with_some_model(self):
        confirmation = EmailConfirmation.objects.set_email_for_object(
            email=self.your_customer_support_email,
            content_object=self.your_obj,
            email_field_name='customer_support_email'
        )

        self.assertEqual(confirmation.content_object, self.your_obj)
        self.assertEqual(confirmation.email, self.your_customer_support_email)
        self.assertEqual(confirmation.email_field_name, 'customer_support_email')

        mail_obj = mail.outbox[0]

        self.assertIn(confirmation.confirmation_key, mail_obj.body)
        self.assertIn(self.your_customer_support_email, mail_obj.body)

        confirmation.confirm()

        self.assertTrue(confirmation.is_verified)
        self.assertEqual(getattr(self.your_obj, 'customer_support_email'), self.your_customer_support_email)

    def test_set_email_for_object_with_is_primary(self):
        kwargs = {
            'content_object': self.user_obj,
            'email_field_name': 'email',
        }

        EmailConfirmation.objects.set_email_for_object(
            email=self.user_email,
            content_object=self.user_obj,
            is_primary=True
        )

        self.assertEqual(EmailConfirmation.objects.get_primary_for_object(**kwargs).email, self.user_email)

        EmailConfirmation.objects.set_email_for_object(
            email=self.user_email_2,
            content_object=self.user_obj,
            is_primary=True
        )

        self.assertEqual(EmailConfirmation.objects.get_primary_for_object(**kwargs).email, self.user_email_2)

        self.assertEqual(EmailConfirmation.objects.get_queryset_for_object(**kwargs).count(), 2)

    def test_set_email_for_object_with_skip_verify(self):
        confirmation = EmailConfirmation.objects.set_email_for_object(
            email=self.user_email,
            content_object=self.user_obj,
            skip_verify=True
        )

        self.assertTrue(confirmation.is_verified)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(self.user_obj.email, self.user_email)


class ModelTest(BaseTestCase):

    def setUp(self):
        self.user_obj = User.objects.create_user(username='kiko_mizuhara')
        self.user_email = 'kiko.mizuhara@gmail.com'
        self.user_email_2 = 'kiko.mizuhara@yahoo.com'

    def test_confirm(self):
        confirmation = EmailConfirmation.objects.set_email_for_object(
            email=self.user_email,
            content_object=self.user_obj,
        )

        with freeze_time("3000-01-01"):
            with self.assertRaises(EmailConfirmationExpired):
                confirmation.confirm()


class CommandTest(BaseTestCase):

    def test_clear_expired_email_confirmations(self):
        mommy.make(
            'email_confirm_la.EmailConfirmation',
            _quantity=1,
            is_verified=False,
            send_at=timezone.now()
        )

        mommy.make(
            'email_confirm_la.EmailConfirmation',
            _quantity=1,
            is_verified=True,
            send_at=timezone.now()
        )

        self.assertEqual(EmailConfirmation.objects.all().count(), 2)

        with freeze_time("3000-01-01"):
            call_command('clear_expired_email_confirmations')

            self.assertEqual(EmailConfirmation.objects.all().count(), 1)
