# coding: utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'email_confirm_la.views',
    url(r'^key/(?P<confirmation_key>\w+)/$', 'confirm_email', name='confirm_email'),
)
