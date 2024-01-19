from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^your_confirm_email/(?P<confirmation_key>\w+)/$', views.your_confirm_email, name='your_confirm_email'),
]
