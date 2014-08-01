# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Achievment.sort_number'
        db.add_column(u'achievments_achievment', 'sort_number',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Achievment.sort_number'
        db.delete_column(u'achievments_achievment', 'sort_number')


    models = {
        u'achievments.achievment': {
            'Meta': {'object_name': 'Achievment'},
            'check': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['achievments.Check']", 'unique': 'True'}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sort_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'achievments.check': {
            'Meta': {'object_name': 'Check'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'test_code': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['achievments']