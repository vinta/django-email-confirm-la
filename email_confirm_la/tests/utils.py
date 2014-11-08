# coding: utf-8

from django.conf import settings
from django.db.models import get_model


user_model_label = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

try:
    from django.contrib.auth import get_user_model
except ImportError:
    def get_user_model():
        return get_model(*user_model_label.rsplit('.', 1))
