# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Check'
        db.create_table(u'achievments_check', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test_code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'achievments', ['Check'])

        # Adding model 'Achievment'
        db.create_table(u'achievments_achievment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('check', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['achievments.Check'], unique=True)),
        ))
        db.send_create_signal(u'achievments', ['Achievment'])


    def backwards(self, orm):
        # Deleting model 'Check'
        db.delete_table(u'achievments_check')

        # Deleting model 'Achievment'
        db.delete_table(u'achievments_achievment')


    models = {
        u'achievments.achievment': {
            'Meta': {'object_name': 'Achievment'},
            'check': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['achievments.Check']", 'unique': 'True'}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'achievments.check': {
            'Meta': {'object_name': 'Check'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'test_code': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['achievments']