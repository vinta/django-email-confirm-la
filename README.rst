django-email-confirm-la
=======================

.. image:: http://img.shields.io/travis/vinta/django-email-confirm-la/master.svg?style=flat-square
    :alt: Build Badge
    :target: https://travis-ci.org/vinta/django-email-confirm-la

.. image:: http://img.shields.io/coveralls/vinta/django-email-confirm-la/master.svg?style=flat-square
    :alt: Coverage Badge
    :target: https://coveralls.io/r/vinta/django-email-confirm-la

.. image:: http://img.shields.io/pypi/v/django-email-confirm-la.svg?style=flat-square
    :alt: Version Badge
    :target: https://pypi.python.org/pypi/django-email-confirm-la

Django email confirmation for any Model and any Field.

Requirements
============

- Python (2.6, 2.7, 3.3, 3.4)
- Django (1.4, 1.5, 1.6, 1.7)

Installation
============

.. code-block:: bash

    $ pip install django-email-confirm-la


In your ``settings.py``:

Add the ``email_confirm_la`` app (put it *after* your apps) and set the required settings:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'email_confirm_la',
        ...
    )

    DEFAULT_FROM_EMAIL = 'hello@your-domain.com'
    EMAIL_CONFIRM_LA_HTTP_PROTOCOL = 'http'
    EMAIL_CONFIRM_LA_DOMAIN = 'your-domain.com'

If you are using the `sites <https://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_ framework, then ``EMAIL_CONFIRM_LA_DOMAIN`` can be omitted and ``Site.objects.get_current().domain`` will be used.

In your ``urls.py``:

.. code-block:: python

    urlpatterns = patterns(
        '',
        url(r'^email_confirmation/', include('email_confirm_la.urls')),
        ...
    )

then run

.. code-block:: bash

    $ python manage.py syncdb
    $ python manage.py migrate

Models
======

For User Model
==============

.. code-block:: python

    from django.contrib.auth.models import User
    from email_confirm_la.models import EmailConfirmation

    user = User.objects.get(username='vinta')
    unconfirmed_email = 'vinta.chen@gmail.com'

    email_confirmation = EmailConfirmation.objects.set_email_for_object(
        email=unconfirmed_email,
        content_object=user,
    )

For Any Model And Any Field
===========================

Assumed you have a model:

.. code-block:: python

    from django.db import models
    from django.contrib.contenttypes.fields import GenericRelation  # Django 1.7+
    from django.contrib.contenttypes.generic import GenericRelation

    class YourModel(models.Model):
        ...
        customer_support_email = models.EmailField(max_length=255, null=True, blank=True)
        marketing_email = models.EmailField(max_length=255, null=True, blank=True)
        ...

        # optional, but recommended when you want to perform cascade-deletions
        email_confirmations = GenericRelation('email_confirm_la.EmailConfirmation', content_type_field='content_type', object_id_field='object_id')

And you want to confirm some emails:

.. code-block:: python

    from your_app.models import YourModel
    from email_confirm_la.models import EmailConfirmation

    some_model_instance = YourModel.objects.get(id=42)

    email_confirmation = EmailConfirmation.objects.set_email_for_object(
        email='marvin@therestaurantattheendoftheuniverse.com',
        content_object=some_model_instance,
        email_field_name='customer_support_email'
    )

    email_confirmation = EmailConfirmation.objects.set_email_for_object(
        email='arthur.dent@therestaurantattheendoftheuniverse.com',
        content_object=some_model_instance,
        email_field_name='marketing_email'
    )

Signals
=======

- ``post_email_confirmation_send``
- ``post_email_confirm``
- ``post_email_save``

In your ``models.py``:

.. code-block:: python

    from django.dispatch import receiver
    from email_confirm_la.signals import post_email_confirm

    @receiver(post_email_confirm)
    def post_email_confirm_callback(sender, confirmation, **kwargs):
        model_instace = confirmation.content_object
        email = confirmation.email

        do_your_stuff()

Commands
========

.. code-block:: bash

    $ python manage.py clear_expired_email_confirmations

Templates
=========

You will want to override the project's email text and confirmation page.

Ensure the ``email_confirm_la`` app in ``INSTALLED_APPS`` is after the app that you will place the customized templates in so that the `django.template.loaders.app_directories.Loader <https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.app_directories.Loader>`_ finds *your* templates before the default templates.

Then copy the templates into your app:

.. code-block:: bash

    $ cp -R django-email-confirm-la/email_confirm_la/templates/email_confirm_la your_app/templates/email_confirm_la

Finally, modify them:

* ``email/email_confirmation_subject.txt``: Produces the subject line of the email.
* ``email/email_confirmation_message.html``: The HTML body of the email.
* ``email_confirm_success.html``: What the user sees after clicking a confirmation link (on success).
* ``email_confirm_fail.html:`` What the user sees after clicking a confirmation link that has expired or is invalid.

Settings
========

Default values of app settings:

.. code-block:: python

    EMAIL_CONFIRM_LA_EMAIL_BACKEND = settings.EMAIL_BACKEND
    EMAIL_CONFIRM_LA_HTTP_PROTOCOL = 'http'
    EMAIL_CONFIRM_LA_DOMAIN = ''  # remember to override this setting!
    EMAIL_CONFIRM_LA_CONFIRM_EXPIRE_SEC = 60 * 60 * 24 * 1  # 1 day
    EMAIL_CONFIRM_LA_CONFIRM_URL_REVERSE_NAME = 'confirm_email'
    EMAIL_CONFIRM_LA_SAVE_EMAIL_TO_INSTANCE = True

Run Tests
=========

.. code-block:: bash

    $ pip install -r requirements_test.txt
    $ python setup.py test
