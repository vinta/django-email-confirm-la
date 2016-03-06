# coding: utf-8

import django


__all__ = ['GenericForeignKey', 'update_fields']


if django.VERSION >= (1, 7):
    from django.contrib.contenttypes.fields import GenericForeignKey
else:
    from django.contrib.contenttypes.generic import GenericForeignKey

if django.VERSION >= (1, 5):
    update_fields = lambda instance, fields: instance.save(update_fields=fields)
else:
    update_fields = lambda instance, fields: instance.save()
