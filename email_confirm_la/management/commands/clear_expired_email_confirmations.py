# coding: utf-8

import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from email_confirm_la.conf import configs
from email_confirm_la.models import EmailConfirmation


class Command(BaseCommand):

    def handle(self, **options):
        expiration_time = timezone.now() - datetime.timedelta(seconds=configs.EMAIL_CONFIRM_LA_CONFIRM_EXPIRE_SEC)
        EmailConfirmation.objects.filter(send_at__lt=expiration_time).delete()
