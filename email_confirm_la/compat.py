# coding: utf-8

from django.db import transaction
import django


__all__ = ['transaction', 'update_fields']


if django.VERSION < (1, 6):
    transaction.atomic = transaction.commit_on_success

if django.VERSION >= (1, 5):
    update_fields = lambda instance, fields: instance.save(update_fields=fields)
else:
    update_fields = lambda instance, fields: instance.save()
