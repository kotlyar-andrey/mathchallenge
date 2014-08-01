# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('src.challenge.views',
    url(r'^$', 'index', name='index'),
    url(r'^challenge_change/$', 'challenge_change'),
    url(r'^kenguru_check/$', 'kenguru_check'),
    url(r'^(?P<category_slug>\w+)/$', 'challenge', name='challenge'),
)