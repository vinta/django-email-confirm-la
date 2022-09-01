# coding: utf-8

from django.urls import re_path
from email_confirm_la.views import confirm_email


urlpatterns = [
    re_path(r'^key/(?P<confirmation_key>\w+)/$', confirm_email, name='confirm_email'),
]
