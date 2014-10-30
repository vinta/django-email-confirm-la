# coding: utf-8


def get_version():
    return '.'.join((str(number) for number in VERSION))


VERSION = (0, 1, 0)

__version__ = get_version()
