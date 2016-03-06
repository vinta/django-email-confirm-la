# coding: utf-8

import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.core.mail import get_connection
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import pgettext_lazy as _

from email_confirm_la import signals
from email_confirm_la import utils
from email_confirm_la.compat import GenericForeignKey
from email_confirm_la.compat import update_fields
from email_confirm_la.conf import settings
from email_confirm_la.exceptions import EmailConfirmationExpired


class EmailConfirmationManager(models.Manager):

    def set_email_for_object(self, email, content_object, email_field_name='email', skip_verify=False, template_context=None):
        """
        Add an email for `content_object` and send a confirmation mail by default.

        The email will be directly saved to `content_object.email_field_name` when `is_primary` and `skip_verify` both are true.
        """

        content_type = ContentType.objects.get_for_model(content_object)
        try:
            confirmation = EmailConfirmation.objects.get(
                content_type=content_type,
                object_id=content_object.id,
                email_field_name=email_field_name,
                email=email,
            )
        except EmailConfirmation.DoesNotExist:
            confirmation = EmailConfirmation()
            confirmation.content_object = content_object
            confirmation.email_field_name = email_field_name
            confirmation.email = email
            confirmation.confirmation_key = utils.generate_random_token([str(content_type.id), str(content_object.id), email, ])
            confirmation.save()

        if skip_verify:
            confirmation.confirm(ignore_expire=True)
        else:
            confirmation.send(template_context)

        return confirmation

    def get_queryset_for_object(self, content_object, email_field_name='email'):
        content_type = ContentType.objects.get_for_model(content_object)
        queryset = EmailConfirmation.objects.filter(content_type=content_type, object_id=content_object.id, email_field_name=email_field_name)

        return queryset

    def get_for_object(self, content_object, email_field_name='email'):
        content_type = ContentType.objects.get_for_model(content_object)
        confirmation = EmailConfirmation.objects.get(content_type=content_type, object_id=content_object.id, email_field_name=email_field_name)

        return confirmation


class EmailConfirmation(models.Model):
    """
    Once an email is confirmed, it will be delete from this model. In other words, there are only unconfirmed emails in the database.
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    email_field_name = models.CharField(verbose_name=_('ec_la', 'Email field name'), max_length=16, default='email')
    email = models.EmailField(verbose_name=_('ec_la', 'Email'))
    confirmation_key = models.CharField(verbose_name=_('ec_la', 'Confirmation_key'), max_length=64, unique=True)
    send_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = _('ec_la', 'Email confirmation')
        verbose_name_plural = _('ec_la', 'Email confirmation')
        # unique_together = (('content_type', 'email_field_name', 'object_id', 'email'), )
        unique_together = (('content_type', 'email_field_name', 'email'), )

    def __str__(self):
        return 'Confirmation for %s' % self.email

    def __unicode__(self):
        return 'Confirmation for %s' % self.email

    def get_confirmation_url(self, full=True, request=None):
        url_reverse_name = settings.EMAIL_CONFIRM_LA_CONFIRM_URL_REVERSE_NAME
        url = reverse(url_reverse_name, kwargs={'confirmation_key': self.confirmation_key})

        if full:
            # TODO: use request.build_absolute_uri()
            final_url = '%s://%s%s' % (
                settings.EMAIL_CONFIRM_LA_HTTP_PROTOCOL,
                settings.EMAIL_CONFIRM_LA_DOMAIN,
                url,
            )
        else:
            final_url = url

        return final_url

    def send(self, template_context=None):
        default_template_context = {
            'email': self.email,
            'confirmation_key': self.confirmation_key,
            'confirmation_url': self.get_confirmation_url(),
        }
        if isinstance(template_context, dict):
            template_context = dict(default_template_context.items() + template_context.items())  # merge dictionaries
        else:
            template_context = default_template_context

        subject = render_to_string('email_confirm_la/email/email_confirmation_subject.txt', template_context)
        subject = ''.join(subject.splitlines())  # remove unnecessary line breaks
        body = render_to_string('email_confirm_la/email/email_confirmation_message.html', template_context)

        message = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [self.email, ])
        message.content_subtype = 'html'
        message.send()

        # connection = get_connection(settings.EMAIL_CONFIRM_LA_EMAIL_BACKEND)
        # connection.send_messages([message, ])

        self.send_at = timezone.now()
        update_fields(self, fields=('send_at', ))

        signals.post_email_confirmation_send.send(
            sender=self.__class__,
            confirmation=self,
        )

    @property
    def is_expired(self):
        if not self.send_at:
            return False

        expiration_time = self.send_at + datetime.timedelta(seconds=settings.EMAIL_CONFIRM_LA_CONFIRM_EXPIRE_SEC)

        return expiration_time <= timezone.now()

    def confirm(self, ignore_expire=False):
        if not ignore_expire and self.is_expired:
            raise EmailConfirmationExpired()

        content_object = self.content_object
        setattr(content_object, self.email_field_name, self.email)
        update_fields(content_object, fields=(self.email_field_name, ))

        signals.post_email_confirmation_confirm.send(
            sender=self.__class__,
            confirmation=self,
        )

        # delete all confirmations for the same email
        EmailConfirmation.objects.filter(content_type=self.content_type, email_field_name=self.email_field_name, email=self.email).delete()
