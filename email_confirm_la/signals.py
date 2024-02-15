# coding: utf-8

from django.dispatch import Signal


# providing args: confirmation
post_email_confirmation_send = Signal()

# providing args: 'confirmation', 'save_to_content_object', 'old_email'
post_email_confirmation_confirm = Signal()
