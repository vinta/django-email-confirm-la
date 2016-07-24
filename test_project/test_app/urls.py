from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^your_confirm_email/(?P<confirmation_key>\w+)/$', views.your_confirm_email, name='your_confirm_email'),
]
