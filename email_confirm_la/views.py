# coding: utf-8

from django.shortcuts import render

from email_confirm_la.models import EmailConfirmation
from email_confirm_la.exceptions import EmailConfirmationExpired


def confirm_email(request, confirmation_key):
    try:
        email_confirmation = EmailConfirmation.objects.get(confirmation_key=confirmation_key)
        email_confirmation.confirm()
    except (EmailConfirmation.DoesNotExist, EmailConfirmationExpired):
        return render(request, 'email_confirm_la/email_confirm_fail.html')

    context = {
        'email_confirmation': email_confirmation,
    }

    return render(request, 'email_confirm_la/email_confirm_success.html', context)
