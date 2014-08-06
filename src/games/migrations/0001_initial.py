# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table(u'games_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('meta_k', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('meta_d', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('script_path', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('style_path', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'games', ['Game'])


    def backwards(self, orm):
        # Deleting model 'Game'
        db.delete_table(u'games_game')


    models = {
        u'games.game': {
            'Meta': {'object_name': 'Game'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
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