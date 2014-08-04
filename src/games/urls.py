# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('src.games.views',
   url(r'^$', 'index', name='index'),
)