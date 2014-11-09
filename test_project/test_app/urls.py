from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^email_confirm/(?P<confirmation_key>\w+)/$', views.your_confirm_email, name='your_confirm_email'),
)
