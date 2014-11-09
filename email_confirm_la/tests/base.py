# coding: utf-8

from __future__ import unicode_literals

from django.test import TestCase


class BaseTestCase(TestCase):
    # urls = 'test_project.test_project.urls'
    urls = 'email_confirm_la.tests.urls'
