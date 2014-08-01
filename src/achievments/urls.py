# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns


urlpatterns = patterns('src.achievments.views',
    url(r'^$', 'index', name='index'),
    # url(r'^challenge_change/$', 'challenge_change'),
)