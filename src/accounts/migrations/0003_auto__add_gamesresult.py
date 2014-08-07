# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GamesResult'
        db.create_table(u'accounts_gamesresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['games.Game'])),
            ('result', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'accounts', ['GamesResult'])

        # Adding M2M table for field games_best on 'UserProgress'
        m2m_table_name = db.shorten_name(u'accounts_userprogress_games_best')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprogress', models.ForeignKey(orm[u'accounts.userprogress'], null=False)),
            ('gamesresult', models.ForeignKey(orm[u'accounts.gamesresult'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprogress_id', 'gamesresult_id'])


    def backwards(self, orm):
        # Deleting model 'GamesResult'
        db.delete_table(u'accounts_gamesresult')

        # Removing M2M table for field games_best on 'UserProgress'
        db.delete_table(db.shorten_name(u'accounts_userprogress_games_best'))


    models = {
        u'accounts.challengeresult': {
            'Meta': {'object_name': 'ChallengeResult'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['problems.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.IntegerField', [], {})
        },
        u'accounts.emailconfirmation': {
            'Meta': {'object_name': 'EmailConfirmation'},
            'confirmation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        },
        u'accounts.gamesresult': {
            'Meta': {'object_name': 'GamesResult'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['games.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.IntegerField', [], {})
        },
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'favorite_problems': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'fav'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['problems.Problem']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_valid_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'ratings_problems': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'rat'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['problems.Problem']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'accounts.userprogress': {
            'Meta': {'object_name': 'UserProgress'},
            'achievments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'achievments'", 'default': 'None', 'to': u"orm['achievments.Achievment']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'challenge_best': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': u"orm['accounts.ChallengeResult']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'games_best': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': u"orm['accounts.GamesResult']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lessons_solved_lessons': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'lessons_solved_lesson'", 'default': 'None', 'to': u"orm['lessons.Lesson']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'lessons_solved_tasks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'lessons_solved_task'", 'default': 'None', 'to': u"orm['lessons.Task']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'lessons_solved_themes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'lessons_solved_theme'", 'default': 'None', 'to': u"orm['lessons.Theme']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'problems_solved_problems': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'problems_solved_problem'", 'default': 'None', 'to': u"orm['problems.Problem']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.User']", 'unique': 'True'})
        },
        u'achievments.achievment': {
            'Meta': {'ordering': "('sort_number', 'title')", 'object_name': 'Achievment'},
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
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        },
        u'lessons.lesson': {
            'Meta': {'object_name': 'Lesson'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.TextField', [], {}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'test': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lessons.Theme']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'lessons.task': {
            'Meta': {'object_name': 'Task'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lessons.Lesson']"}),
            'slog': ('django.db.models.fields.IntegerField', [], {'default': "'1'"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'lessons.theme': {
            'Meta': {'object_name': 'Theme'},
            'complit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.IntegerField', [], {}),
            'sort_number': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'problems.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['problems.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'sort_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'problems.problem': {
            'Meta': {'object_name': 'Problem'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['problems.Category']"}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ist': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'klass': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slogn': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'solved': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['accounts']