# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailConfirmation'
        db.create_table('email_confirm_la_emailconfirmation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('email_field_name', self.gf('django.db.models.fields.CharField')(max_length=32, default='email')),
            ('email', self.gf('django.db.models.fields.EmailField')(db_index=True, max_length=75)),
            ('confirmation_key', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True)),
            ('send_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, db_index=True, null=True)),
        ))
        db.send_create_signal('email_confirm_la', ['EmailConfirmation'])

        # Adding unique constraint on 'EmailConfirmation', fields ['content_type', 'object_id', 'email_field_name']
        db.create_unique('email_confirm_la_emailconfirmation', ['content_type_id', 'object_id', 'email_field_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'EmailConfirmation', fields ['content_type', 'object_id', 'email_field_name']
        db.delete_unique('email_confirm_la_emailconfirmation', ['content_type_id', 'object_id', 'email_field_name'])

        # Deleting model 'EmailConfirmation'
        db.delete_table('email_confirm_la_emailconfirmation')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'email_confirm_la.emailconfirmation': {
            'Meta': {'object_name': 'EmailConfirmation', 'unique_together': "(('content_type', 'object_id', 'email_field_name'),)"},
            'confirmation_key': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'email': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '75'}),
            'email_field_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'default': "'email'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'send_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['email_confirm_la']