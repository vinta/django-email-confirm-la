# coding: utf-8

from django.conf.urls import url
from .views import confirm_email


urlpatterns = [
    url(r'^key/(?P<confirmation_key>\w+)/$', confirm_email, name='confirm_email'),
]
