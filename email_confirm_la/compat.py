# coding: utf-8

import django


__all__ = ['GenericForeignKey', ]


if django.VERSION >= (1, 7):
    from django.contrib.contenttypes.fields import GenericForeignKey
else:
    from django.contrib.contenttypes.generic import GenericForeignKey
