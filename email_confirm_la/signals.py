# coding: utf-8

from __future__ import unicode_literals

import django.dispatch


post_email_confirmation_send = django.dispatch.Signal(providing_args=['confirmation', ])
post_email_confirm = django.dispatch.Signal(providing_args=['confirmation', ])
post_email_save = django.dispatch.Signal(providing_args=['confirmation', ])
