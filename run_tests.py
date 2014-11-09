# coding: utf-8

import os
import sys

parent_dir = os.path.dirname(os.path.abspath(__file__))  # will be: /path/to/django-email-confirm-la/
sys.path.insert(0, os.path.join(parent_dir, 'email_confirm_la/'))
sys.path.insert(1, os.path.join(parent_dir, 'test_project/'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'

from django.conf import settings
import django


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
