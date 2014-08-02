# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url


urlpatterns = patterns('src.main.views',
    url(r'^$', 'index', name='index'),
    url(r'^achievments_check/$', 'achievments_check', name='achievments_check'),
    url(r'^feedback/$', 'feedback', name='feedback'),
)