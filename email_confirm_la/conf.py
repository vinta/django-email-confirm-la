# coding: utf-8

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from appconf import AppConf


class ECLAAppConf(AppConf):
    EMAIL_BACKEND = settings.EMAIL_BACKEND
    HTTP_PROTOCOL = 'http'
    DOMAIN = ''
    CONFIRM_EXPIRE_SEC = 60 * 60 * 24 * 1  # 1 day
    CONFIRM_URL_REVERSE_NAME = 'confirm_email'

    # TODO: EMAIL UNIQUE OR NOT
    # unique_together = (('content_type', 'email_field_name', 'email'), )

    class Meta:
        prefix = 'email_confirm_la'

    def configure_domain(self, value):
        from django.contrib.sites.models import Site

        if not value:
            try:
                current_site = Site.objects.get_current()
            except ImproperlyConfigured:
                raise ImproperlyConfigured("You need to provide `EMAIL_CONFIRM_LA_DOMAIN` in settings if you don't use the sites framework.")
            else:
                value = current_site.domain

        return value
