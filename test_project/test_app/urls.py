from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^key/(?P<confirmation_key>\w+)/$', views.your_confirm_email, name='your_confirm_email'),
)
