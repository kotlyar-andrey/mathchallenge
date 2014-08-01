# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('src.lessons.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<theme_pk>\d+)/$', 'theme', name='theme'),
    url(r'^(?P<theme_pk>\d+)/lesson/(?P<lesson_number>\d+)/$', 'lesson', name='lesson'),
    url(r'^check/$', 'answer_check'),
)