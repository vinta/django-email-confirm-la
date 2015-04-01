# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'EmailConfirmation', fields ['content_type', 'email_field_name', 'email']
        db.delete_unique(u'email_confirm_la_emailconfirmation', ['content_type_id', 'email_field_name', 'email'])

        # Adding unique constraint on 'EmailConfirmation', fields ['content_type', 'email_field_name', 'object_id', 'email']
        db.create_unique(u'email_confirm_la_emailconfirmation', ['content_type_id', 'email_field_name', 'object_id', 'email'])


    def backwards(self, orm):
        # Removing unique constraint on 'EmailConfirmation', fields ['content_type', 'email_field_name', 'object_id', 'email']
        db.delete_unique(u'email_confirm_la_emailconfirmation', ['content_type_id', 'email_field_name', 'object_id', 'email'])

        # Adding unique constraint on 'EmailConfirmation', fields ['content_type', 'email_field_name', 'email']
        db.create_unique(u'email_confirm_la_emailconfirmation', ['content_type_id', 'email_field_name', 'email'])


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'email_confirm_la.emailconfirmation': {
            'Meta': {'unique_together': "((u'content_type', u'email_field_name', u'object_id', u'email'),)", 'object_name': 'EmailConfirmation'},
            'confirmation_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'confirmed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'email_field_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'send_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['email_confirm_la']