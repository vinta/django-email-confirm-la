# coding: utf-8

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import pgettext_lazy as _

from email_confirm_la.models import EmailConfirmation


class AuthUserEmailValidator(EmailValidator):

    def __call__(self, value):
        super(AuthUserEmailValidator, self).__call__(value)

        from django.contrib.auth.models import User

        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError(_('ecla', 'This email has already been taken.'))


class EmailConfirmationValidator(EmailValidator):

    def __init__(self, content_object_model, email_field_name='email', regex=None, message=None, code=None):
        super(EmailConfirmationValidator, self).__init__(regex, message, code)

        self.content_type = ContentType.objects.get_for_model(content_object_model)
        self.email_field_name = email_field_name

    def __call__(self, value):
        super(EmailConfirmationValidator, self).__call__(value)

        email_exists = EmailConfirmation.objects \
            .filter(content_type=self.content_type, email_field_name=self.email_field_name) \
            .filter(email__iexact=value) \
            .exists()
        if email_exists:
            raise ValidationError(_('ecla', 'This email has already been taken.'))
