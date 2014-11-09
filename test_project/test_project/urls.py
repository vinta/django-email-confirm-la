from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^email_confirmation/', include('email_confirm_la.urls')),
    url(r'^test_app/', include('test_app.urls', namespace='test_app')),
)
