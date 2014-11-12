# coding: utf-8

from __future__ import unicode_literals
import datetime

try:
    # Django 1.7+ compatibility
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey

from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage, get_connection
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import pgettext_lazy as _

from email_confirm_la import signals
from email_confirm_la import utils
from email_confirm_la.compat import update_fields, transaction
from email_confirm_la.conf import settings
from email_confirm_la.exceptions import EmailConfirmationExpired


class EmailConfirmationManager(models.Manager):

    def set_email_for_object(self, email, content_object, email_field_name='email', is_primary=True, skip_verify=False, template_context=None):
        """
        只有 `is_primary=True` 時，email 才會被 save 到 content_object 的 email_field_name 欄位
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

            if not skip_verify:
                confirmation.send(template_context)

        if is_primary:
            confirmation = confirmation.set_primary()

        if skip_verify:
            confirmation.is_verified = True
            # confirmation.save(update_fields=['is_verified', ])
            update_fields(confirmation, fields=('is_verified', ))

        if confirmation.is_verified and confirmation.is_primary and settings.EMAIL_CONFIRM_LA_SAVE_EMAIL_TO_INSTANCE:
            confirmation.save_email()

        return confirmation

    def get_queryset_for_object(self, content_object, email_field_name='email'):
        content_type = ContentType.objects.get_for_model(content_object)
        queryset = EmailConfirmation.objects.filter(content_type=content_type, object_id=content_object.id, email_field_name=email_field_name)

        return queryset

    def get_primary_for_object(self, content_object, email_field_name='email'):
        confirmation = self.get_queryset_for_object(content_object, email_field_name).get(is_primary=True)

        return confirmation


class EmailConfirmation(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    email_field_name = models.CharField(verbose_name=_('ec_la', 'Email field name'), max_length=32)
    email = models.EmailField(verbose_name=_('ec_la', 'Email'), max_length=255)
    confirmation_key = models.CharField(verbose_name=_('ec_la', 'Confirmation_key'), max_length=64, unique=True)
    is_primary = models.BooleanField(verbose_name=_('ec_la', 'Is primary'), default=False)
    is_verified = models.BooleanField(verbose_name=_('ec_la', 'Is verified'), default=False)
    send_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = _('ec_la', 'Email confirmation')
        verbose_name_plural = _('ec_la', 'Email confirmation')
        unique_together = (('content_type', 'email_field_name', 'email'), )

    def __unicode__(self):
        return 'Confirmation for %s' % self.email

    def set_primary(self):
        try:
            old_primary = EmailConfirmation.objects.get_primary_for_object(content_object=self.content_object, email_field_name=self.email_field_name)
        except EmailConfirmation.DoesNotExist:
            pass
        else:
            if old_primary != self:
                old_primary.is_primary = False
                # old_primary.save(update_fields=['is_primary', ])
                update_fields(old_primary, fields=('is_primary', ))

        self.is_primary = True
        # self.save(update_fields=['is_primary', ])
        update_fields(self, fields=('is_primary', ))

        return self

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
        subject = ''.join(subject.splitlines())  # remove superfluous line breaks
        body = render_to_string('email_confirm_la/email/email_confirmation_message.html', template_context)

        message = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [self.email, ])
        message.content_subtype = 'html'
        # message.send()

        # TODO: send mass emails?
        connection = get_connection(settings.EMAIL_CONFIRM_LA_EMAIL_BACKEND)
        connection.send_messages([message, ])

        self.send_at = timezone.now()
        # self.save(update_fields=['send_at', ])
        update_fields(self, fields=('send_at', ))

        signals.post_email_confirmation_send.send(
            sender=self.__class__,
            confirmation=self,
        )

    def is_expired(self):
        expiration_time = self.send_at + datetime.timedelta(seconds=settings.EMAIL_CONFIRM_LA_CONFIRM_EXPIRE_SEC)
        return expiration_time <= timezone.now()
    is_expired.boolean = True

    def save_email(self):
        content_object = self.content_object
        email_field_name = self.email_field_name
        email = self.email

        setattr(content_object, email_field_name, email)
        # content_object.save(update_fields=[email_field_name, ])
        update_fields(content_object, fields=(email_field_name, ))

        signals.post_email_save.send(
            sender=self.__class__,
            confirmation=self,
        )

    def confirm(self):
        if self.is_expired():
            raise EmailConfirmationExpired()
        else:
            if not self.is_verified:
                with transaction.atomic():
                    self.is_verified = True
                    self.confirmed_at = timezone.now()
                    # self.save(update_fields=['is_verified', 'confirmed_at'])
                    update_fields(self, fields=('is_verified', 'confirmed_at'))

                    signals.post_email_confirm.send(
                        sender=self.__class__,
                        confirmation=self,
                    )

                    if self.is_primary and settings.EMAIL_CONFIRM_LA_SAVE_EMAIL_TO_INSTANCE:
                        self.save_email()

        return self
