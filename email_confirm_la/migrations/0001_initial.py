# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('email_field_name', models.CharField(verbose_name='Email field name', max_length=32)),
                ('email', models.EmailField(verbose_name='Email', max_length=255)),
                ('confirmation_key', models.CharField(verbose_name='Confirmation_key', max_length=64, unique=True)),
                ('is_primary', models.BooleanField(verbose_name='Is primary', default=False)),
                ('is_verified', models.BooleanField(verbose_name='Is verified', default=False)),
                ('send_at', models.DateTimeField(null=True, blank=True)),
                ('confirmed_at', models.DateTimeField(null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Email confirmation',
                'verbose_name_plural': 'Email confirmation',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='emailconfirmation',
            unique_together=set([('content_type', 'email_field_name', 'email')]),
        ),
    ]
