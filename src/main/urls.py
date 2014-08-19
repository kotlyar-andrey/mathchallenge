# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('src.main.views',
    url(r'^$', 'index', name='index'),
    url(r'^achievments_check/$', 'achievments_check', name='achievments_check'),
    url(r'^feedback/$', 'feedback', name='feedback'),
    url(r'robots.txt$', TemplateView.as_view(template_name='main/robots.txt', content_type='text/plain')),
)