# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('src.problems.views',
    url(r'^$', 'index', name='index'),
    url(r'^category/(?P<category_slug>\w+)/$', 'category', name='category'),
    url(r'^problem/(?P<problem_pk>\d+)/$', 'problem', name='problem'),
    url(r'^board/$', 'board', name='board'),
    url(r'^add_fav/(?P<problem_pk>\d+)/$', 'add_fav', name='add_fav'),
    url(r'^numbering/$', 'pr_numbering', name='pr_numbering'),
    url(r'errortest/$', 'error_test'),
)