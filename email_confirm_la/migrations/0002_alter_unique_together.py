# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email_confirm_la', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='emailconfirmation',
            unique_together=set([('content_type', 'email_field_name', 'object_id', 'email', )]),
        ),
    ]
