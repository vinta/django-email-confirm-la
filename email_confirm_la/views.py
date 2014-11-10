# coding: utf-8

from __future__ import unicode_literals

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from email_confirm_la.models import EmailConfirmation


def confirm_email(request, confirmation_key):
    try:
        email_confirmation = EmailConfirmation.objects.get(confirmation_key=confirmation_key)
    except EmailConfirmation.DoesNotExist:
        # TODO: show a email confirm fail page
        raise Http404

    response = email_confirmation.confirm(request)
    if response:
        return response

    context = {
        'email_confirmation': email_confirmation,
    }

    return render(request, 'email_confirm_la/email_confirm_success.html', context)
