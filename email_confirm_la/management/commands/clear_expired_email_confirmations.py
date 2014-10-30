# coding: utf-8

from django.core.management.base import BaseCommand

from email_confirm_la.models import EmailConfirmation


class Command(BaseCommand):

    def handle(self, **options):
        count = 0
        expired_email_confirmations = EmailConfirmation.objects.filter(is_verified=False)
        for email_confirmation in expired_email_confirmations.iterator():
            if email_confirmation.is_expired():
                email_confirmation.delete()
                count += 1

        print('%s deleted' % count)
