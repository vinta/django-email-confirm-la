# coding: utf-8

import os
import sys

from django.conf import settings
import django


parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dir)

settings.configure(
    DEBUG=False,
    SECRET_KEY='do_not_go_gentle_into_that_good_night',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'email_confirm_la',
    ],
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    ROOT_URLCONF='',
)


def run_tests():
    if hasattr(django, 'setup'):
        django.setup()

    from django.test.utils import get_runner

    test_runner_class = get_runner(settings)
    test_runner = test_runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['email_confirm_la', ])
    sys.exit(failures)


def main():
    run_tests()


if __name__ == '__main__':
    main()
