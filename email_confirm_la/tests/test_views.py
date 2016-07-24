# coding: utf-8

from django.contrib.auth.models import User
from django.core import mail
from django.test.utils import override_settings

from .base import BaseTestCase
from email_confirm_la.models import EmailConfirmation


class ViewTest(BaseTestCase):

    def setUp(self):
        self.user_obj = User.objects.create_user(username='kiko_mizuhara')
        self.user_email = 'kiko.mizuhara@gmail.com'
        self.user_email_2 = 'kiko.mizuhara@yahoo.com'

    def test_confirm_email(self):
        confirmation = EmailConfirmation.objects.verify_email_for_object(
            email=self.user_email,
            content_object=self.user_obj,
        )

        url = confirmation.get_confirmation_url(full=False)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.user_obj = User.objects.get(id=self.user_obj.id)
        self.assertEqual(self.user_obj.email, self.user_email)

    def test_confirm_email_invalid(self):
        confirmation = EmailConfirmation.objects.verify_email_for_object(
            email=self.user_email,
            content_object=self.user_obj,
        )

        confirmation.confirmation_key = 'broken'

        url = confirmation.get_confirmation_url(full=False)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'email_confirm_la/email_confirmation_fail.html'
        )

    @override_settings(EMAIL_CONFIRM_LA_HTTP_PROTOCOL='https', EMAIL_CONFIRM_LA_DOMAIN='vinta.ws')
    def test_custom_domain(self):
        EmailConfirmation.objects.verify_email_for_object(
            email=self.user_email,
            content_object=self.user_obj,
        )

        mail_obj = mail.outbox[0]

        self.assertIn('https://vinta.ws/', mail_obj.body)

    @override_settings(EMAIL_CONFIRM_LA_CONFIRM_URL_REVERSE_NAME='test_app:your_confirm_email')
    def test_custom_confirm_url_reverse_name(self):
        confirmation = EmailConfirmation.objects.verify_email_for_object(
            email=self.user_email,
            content_object=self.user_obj,
        )

        url = confirmation.get_confirmation_url(full=False)

        self.assertIn('/test_app/your_confirm_email/', url)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        confirmation = EmailConfirmation.objects.get(id=confirmation.id)
        self.user_obj = User.objects.get(id=self.user_obj.id)

        self.assertEqual(self.user_obj.email, self.user_email)

    @override_settings(EMAIL_CONFIRM_LA_CONFIRM_URL_REVERSE_NAME='test_app:your_confirm_email')
    def test_custom_template_context_in_email(self):
        EmailConfirmation.objects.verify_email_for_object(
            email=self.user_email,
            content_object=self.user_obj,
        )

        mail_obj = mail.outbox[0]

        self.assertIn('the Answer to the Ultimate Question of Life, the Universe, and Everything: 42.', mail_obj.body)

    def test_custom_template_context_in_view(self):
        confirmation = EmailConfirmation.objects.verify_email_for_object(
            email=self.user_email,
            content_object=self.user_obj,
        )

        url = confirmation.get_confirmation_url(full=False)
        response = self.client.get(url)

        self.assertContains(response, 'the Answer to the Ultimate Question of Life, the Universe, and Everything: 42.')
