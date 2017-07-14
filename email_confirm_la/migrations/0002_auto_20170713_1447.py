# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email_confirm_la', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='email',
            field=models.EmailField(max_length=75, db_index=True, verbose_name='Email'),
            preserve_default=True,
        ),
    ]
