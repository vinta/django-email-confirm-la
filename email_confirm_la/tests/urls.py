# coding: utf-8

import django


if django.VERSION >= (1, 5):
    from django.conf.urls import patterns, include, url
else:
    from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^email_confirmation/', include('email_confirm_la.urls')),
)
