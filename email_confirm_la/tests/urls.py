import django

if django.get_version() >= '1.5':
    from django.conf.urls import patterns, include, url
else:
    from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^email_confirmation/', include('email_confirm_la.urls')),
)
