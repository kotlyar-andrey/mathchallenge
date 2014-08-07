# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('src.games.views',
   url(r'^$', 'index', name='index'),
   url(r'^dev/', 'dev', name='dev'),
   url(r'^(?P<game_pk>\d+)/$', 'game', name='game'),
   url(r'^game_over/$', 'game_over', name='game_over'),
)