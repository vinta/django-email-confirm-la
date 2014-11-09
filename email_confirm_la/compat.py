# coding: utf-8

from django.conf import settings
from django.db import transaction
import django


__all__ = ['update_fields', 'User']


if django.VERSION >= (1, 5):
    update_fields = lambda instance, fields: instance.save(update_fields=fields)

    if django.VERSION >= (1, 7):
        from django.apps import apps

        if apps.ready:
            from django.contrib.auth import get_user_model
            User = get_user_model()
    else:
        from django.contrib.auth import get_user_model
        User = get_user_model()
else:
    update_fields = lambda instance, fields: instance.save()

    from django.contrib.auth.models import User

transaction_atomic = getattr(transaction, 'atomic', 'commit_on_success')

if django.VERSION < (1, 6):
    transaction.atomic = transaction.commit_on_success

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
