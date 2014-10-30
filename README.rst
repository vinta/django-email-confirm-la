django-email-confirm-la
=======================

Django email confirmation for any Model and any Field.

Install
=======

.. code-block:: bash

    $ pip install django-email-confirm-la


in your ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'email_confirm_la',
        ...
    )

    EMAIL_CONFIRMATION_LA_HTTP_PROTOCOL = 'http'
    EMAIL_CONFIRMATION_LA_DOMAIN = 'your-domain.com'

in your ``urls.py``:

.. code-block:: python

    urlpatterns = patterns(
        '',
        url(r'^email_confirmation/', include('email_confirm_la.urls')),
        ...
    )

then run

.. code-block:: bash

    $ python manage.py syncdb

    # or if you use south (you should)
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

assumed you have a model:

.. code-block:: python

    from django.db import models

    class YourModel(models.Model):
        ...
        user_support_email = models.EmailField(max_length=255)
        marketing_email = models.EmailField(max_length=255)
        ...

and you want to confirm some emails:

.. code-block:: python

    from your_app.models import YourModel
    from email_confirm_la.models import EmailConfirmation

    some_model_instance = YourModel.objects.get(id=42)

    email_confirmation = EmailConfirmation.objects.set_email_for_object(
        email='marvin@therestaurantattheendoftheuniverse.com',
        content_object=some_model_instance,
        email_field_name='user_support_email'
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

you can do something like:

.. code-block:: python

    from django.dispatch import receiver
    from email_confirm_la.signals import post_email_confirm

    @receiver(post_email_confirm)
    def post_email_confirm_callback(sender, confirmation, **kwargs):
        model_instace = confirmation.content_object
        email = confirmation.email

        do_stuff()

Commands
========

.. code-block:: bash

    $ python manage.py clear_expired_email_confirmations

Settings
========

Default values of app settings:

.. code-block:: python

    EMAIL_CONFIRM_LA_HTTP_PROTOCOL = 'http'
    EMAIL_CONFIRM_LA_DOMAIN = ''
    EMAIL_CONFIRM_LA_CONFIRM_EXPIRE_SEC = 60 * 60 * 24 * 1  # 1 day
    EMAIL_CONFIRM_LA_CONFIRM_URL_REVERSE_NAME = 'confirm_email'
    EMAIL_CONFIRM_LA_SAVE_EMAIL_TO_INSTANCE = True
