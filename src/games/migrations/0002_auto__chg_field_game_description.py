# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Game.description'
        db.alter_column(u'games_game', 'description', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'Game.description'
        db.alter_column(u'games_game', 'description', self.gf('django.db.models.fields.CharField')(max_length=250))

    models = {
        u'games.game': {
            'Meta': {'object_name': 'Game'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_d': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'meta_k': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'script_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'style_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['games']