# coding: utf-8

VERSION = (4, 0, 0)


def get_version():
    return '.'.join((str(number) for number in VERSION))


__version__ = get_version()

default_app_config = 'email_confirm_la.apps.ECLAAppConf'
