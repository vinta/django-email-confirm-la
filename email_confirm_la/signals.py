# coding: utf-8

import django.dispatch


post_email_confirmation_send = django.dispatch.Signal(providing_args=['confirmation', ])
post_email_confirmation_confirm = django.dispatch.Signal(providing_args=['confirmation', ])
