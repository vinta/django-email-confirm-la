# coding: utf-8

from django.conf import settings


class DefaultConfigs(object):

    EMAIL_CONFIRM_LA_HTTP_PROTOCOL = 'http'
    EMAIL_CONFIRM_LA_DOMAIN = 'example.com'
    EMAIL_CONFIRM_LA_CONFIRM_EXPIRE_SEC = 60 * 60 * 24 * 1  # 1 day
    EMAIL_CONFIRM_LA_CONFIRM_URL_REVERSE_NAME = 'email_confirm_la:confirm_email'
    EMAIL_CONFIRM_LA_TEMPLATE_CONTEXT = {}
    EMAIL_CONFIRM_LA_AUTOLOGIN = False


class Configs(object):

    def __getattr__(self, name):
        default_setting = getattr(DefaultConfigs, name)
        setting = getattr(settings, name, default_setting)

        return setting


configs = Configs()
