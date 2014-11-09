from django.http import Http404
from django.shortcuts import render

from email_confirm_la.models import EmailConfirmation


def your_confirm_email(request, confirmation_key):
    email_confirmation = EmailConfirmation.objects.get(confirmation_key=confirmation_key)
    email_confirmation.confirm()

    context = {
        'email_confirmation': email_confirmation,
    }

    return render(request, 'test_app/your_confirm_email.html', context)
