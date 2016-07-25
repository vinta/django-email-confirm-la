# coding: utf-8

import datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from email_confirm_la import signals
from email_confirm_la.conf import configs
from email_confirm_la.compat import GenericForeignKey
from email_confirm_la.exceptions import ExpiredError
from email_confirm_la.utils import generate_random_token


class EmailConfirmationManager(models.Manager):

    def verify_email_for_object(self, email, content_object, email_field_name='email'):
        """
        Create an email confirmation for `content_object` and send a confirmation mail.

        The email will be directly saved to `content_object.email_field_name` when `is_primary` and `skip_verify` both are true.
        """

        confirmation_key = generate_random_token([str(content_object.__class__.__name__), str(content_object.id), str(email_field_name), email, ])

        try:
            confirmation = EmailConfirmation()
            confirmation.content_object = content_object
            confirmation.email_field_name = email_field_name
            confirmation.email = email
            confirmation.confirmation_key = confirmation_key
            confirmation.save()
        except IntegrityError:
            confirmation = EmailConfirmation.objects.get_for_object(content_object, email_field_name)
            confirmation.email = email
            confirmation.confirmation_key = confirmation_key
            confirmation.save(update_fields=['email', 'confirmation_key'])

        confirmation.send()

        return confirmation

    def get_unverified_email_for_object(self, content_object, email_field_name='email'):
        try:
            confirmation = EmailConfirmation.objects.get_for_object(content_object, email_field_name)
        except EmailConfirmation.DoesNotExist:
            unverified_email = ''
        else:
            unverified_email = confirmation.email

        return unverified_email

    def get_for_object(self, content_object, email_field_name='email'):
        content_type = ContentType.objects.get_for_model(content_object)
        confirmation = EmailConfirmation.objects.get(content_type=content_type, object_id=content_object.id, email_field_name=email_field_name)

        return confirmation

    def get_queryset_for_object(self, content_object, email_field_name='email'):
        content_type = ContentType.objects.get_for_model(content_object)
        queryset = EmailConfirmation.objects.filter(content_type=content_type, object_id=content_object.id, email_field_name=email_field_name)

        return queryset

    def get_for_email(self, email, content_object_model, email_field_name='email'):
        content_type = ContentType.objects.get_for_model(content_object_model)
        confirmation = EmailConfirmation.objects.get(content_type=content_type, email_field_name=email_field_name, email=email)

        return confirmation


class EmailConfirmation(models.Model):
    """
    Once an email is confirmed, it will be delete from this table. In other words, there are only unconfirmed emails in the database.
    """

    ExpiredError = ExpiredError

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    email_field_name = models.CharField(verbose_name=_(u'Email field name'), max_length=32, default='email')
    email = models.EmailField(verbose_name=_(u'Email'), db_index=True)
    confirmation_key = models.CharField(verbose_name=_(u'Confirmation_key'), max_length=64, unique=True)
    send_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = _(u'Email confirmation')
        verbose_name_plural = _(u'Email confirmation')
        unique_together = (('content_type', 'object_id', 'email_field_name'), )

    def __repr__(self):
        return '<EmailConfirmation {0}>'.format(self.email)

    def __str__(self):
        return 'Confirmation for {0}'.format(self.email)

    def __unicode__(self):
        return u'Confirmation for {0}'.format(self.email)

    def send(self, template_context=None):
        default_template_context = dict(configs.EMAIL_CONFIRM_LA_TEMPLATE_CONTEXT)
        default_template_context['email_confirmation'] = self

        if isinstance(template_context, dict):
            template_context = dict(default_template_context.items() + template_context.items())  # merge dictionaries
        else:
            template_context = default_template_context

        subject = render_to_string('email_confirm_la/email/email_confirmation_subject.txt', template_context)
        subject = ''.join(subject.splitlines()).strip()  # remove unnecessary line breaks
        body = render_to_string('email_confirm_la/email/email_confirmation_message.html', template_context)
        message = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [self.email, ])
        message.content_subtype = 'html'
        message.send()

        self.send_at = timezone.now()
        self.save(update_fields=('send_at', ))

        signals.post_email_confirmation_send.send(
            sender=self.__class__,
            confirmation=self,
        )

    def get_confirmation_url(self, full=True):
        url_reverse_name = configs.EMAIL_CONFIRM_LA_CONFIRM_URL_REVERSE_NAME
        url = reverse(url_reverse_name, kwargs={'confirmation_key': self.confirmation_key})
        if full:
            confirmation_url = '{0}://{1}{2}'.format(configs.EMAIL_CONFIRM_LA_HTTP_PROTOCOL, configs.EMAIL_CONFIRM_LA_DOMAIN, url)
        else:
            confirmation_url = url

        return confirmation_url

    def confirm(self, ignore_expiration=False, save_to_content_object=True):
        if not ignore_expiration and self.is_expired:
            raise ExpiredError()

        if save_to_content_object:
            setattr(self.content_object, self.email_field_name, self.email)
            self.content_object.save(update_fields=(self.email_field_name, ))

        signals.post_email_confirmation_confirm.send(
            sender=self.__class__,
            confirmation=self,
            save_to_content_object=save_to_content_object,
        )

    def clean(self):
        """
        delete all confirmations for the same content_object and the same field
        """

        EmailConfirmation.objects.filter(content_type=self.content_type, object_id=self.object_id, email_field_name=self.email_field_name).delete()

    @property
    def is_expired(self):
        if not self.send_at:
            return False

        expiration_time = self.send_at + datetime.timedelta(seconds=configs.EMAIL_CONFIRM_LA_CONFIRM_EXPIRE_SEC)

        return expiration_time <= timezone.now()
