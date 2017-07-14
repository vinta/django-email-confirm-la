# coding: utf-8

VERSION = (2, 3, 1)


def get_version():
    return '.'.join((str(number) for number in VERSION))


__version__ = get_version()

default_app_config = 'email_confirm_la.apps.ECLAAppConf'
