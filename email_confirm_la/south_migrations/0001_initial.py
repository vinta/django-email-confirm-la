# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailConfirmation'
        db.create_table(u'email_confirm_la_emailconfirmation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('email_field_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('confirmation_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('send_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('confirmed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'email_confirm_la', ['EmailConfirmation'])

        # Adding unique constraint on 'EmailConfirmation', fields ['content_type', 'email_field_name', 'email']
        db.create_unique(u'email_confirm_la_emailconfirmation', ['content_type_id', 'email_field_name', 'email'])


    def backwards(self, orm):
        # Removing unique constraint on 'EmailConfirmation', fields ['content_type', 'email_field_name', 'email']
        db.delete_unique(u'email_confirm_la_emailconfirmation', ['content_type_id', 'email_field_name', 'email'])

        # Deleting model 'EmailConfirmation'
        db.delete_table(u'email_confirm_la_emailconfirmation')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'email_confirm_la.emailconfirmation': {
            'Meta': {'unique_together': "((u'content_type', u'email_field_name', u'email'),)", 'object_name': 'EmailConfirmation'},
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