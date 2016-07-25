# coding: utf-8

from django.dispatch import Signal


post_email_confirmation_send = Signal(providing_args=['confirmation', ])
post_email_confirmation_confirm = Signal(providing_args=['confirmation', 'save_to_content_object', 'old_email'])
