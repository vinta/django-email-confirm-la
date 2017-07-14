# coding: utf-8

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.utils import timezone

from freezegun import freeze_time
from model_mommy import mommy

from .base import BaseTestCase
from email_confirm_la.models import EmailConfirmation
from test_app.models import YourModel


class ManagerTest(BaseTestCase):

    def setUp(self):
        User = get_user_model()
        self.user_obj = User.objects.create_user(username='kiko_mizuhara')
        self.user_obj_2 = User.objects.create_user(username='odyx')
        self.user_email = 'kiko.mizuhara@gmail.com'
        self.user_email_2 = 'kiko.mizuhara@yahoo.com'

        self.your_obj = YourModel.objects.create()
        self.your_customer_support_email = 'marvin@therestaurantattheendoftheuniverse.com'
        self.your_marketing_email = 'arthur@therestaurantattheendoftheuniverse.com'

    def test_verify_email_for_object_with_user_model(self):
        confirmation = EmailConfirmation.objects.verify_email_for_object(
            email=self.user_email,
            content_object=self.user_obj,
        )

        self.assertEqual(confirmation.content_object, self.user_obj)
        self.assertEqual(confirmation.email, self.user_email)
        self.assertEqual(confirmation.email_field_name, 'email')

        mail_obj = mail.outbox[0]

        self.assertIn(confirmation.confirmation_key, mail_obj.body)
        self.assertIn(self.user_email, mail_obj.body)

        confirmation.confirm()

        self.assertEqual(self.user_obj.email, self.user_email)

    def test_verify_email_for_object_with_some_model(self):
        confirmation = EmailConfirmation.objects.verify_email_for_object(
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

        self.assertEqual(getattr(self.your_obj, 'customer_support_email'), self.your_customer_support_email)

    def test_request_the_same_email_by_two_users(self):
        the_same_email = self.user_email

        confirmation_1 = EmailConfirmation.objects.verify_email_for_object(
            email=the_same_email,
            content_object=self.user_obj,
        )
        confirmation_2 = EmailConfirmation.objects.verify_email_for_object(
            email=the_same_email,
            content_object=self.user_obj_2,
        )
        self.assertTrue(confirmation_1.email, the_same_email)
        self.assertTrue(confirmation_2.email, the_same_email)

        confirmation_2.confirm()

        self.assertEqual(self.user_obj_2.email, the_same_email)


class ModelTest(BaseTestCase):

    def setUp(self):
        User = get_user_model()
        self.user_obj = User.objects.create_user(username='kiko_mizuhara')
        self.user_email = 'kiko.mizuhara@gmail.com'
        self.user_email_2 = 'kiko.mizuhara@yahoo.com'

    def test_confirm(self):
        confirmation = EmailConfirmation.objects.verify_email_for_object(
            email=self.user_email,
            content_object=self.user_obj,
        )

        with freeze_time("3000-01-01"):
            with self.assertRaises(EmailConfirmation.ExpiredError):
                confirmation.confirm()


class CommandTest(BaseTestCase):

    def test_clear_expired_email_confirmations(self):
        mommy.make(
            'email_confirm_la.EmailConfirmation',
            _quantity=1,
            send_at=timezone.now()
        )

        self.assertEqual(EmailConfirmation.objects.all().count(), 1)

        with freeze_time("3000-01-01"):
            call_command('clear_expired_email_confirmations')

            self.assertEqual(EmailConfirmation.objects.all().count(), 0)
