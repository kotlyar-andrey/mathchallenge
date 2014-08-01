# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns


urlpatterns = patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'accounts/login.html'}, 'login'),
)

urlpatterns += patterns('src.accounts.views',
    url(r'^create/$', 'create', name='create'),
    url(r'^logout', 'logout', name='logout'),
    url(r'^confirm_email/(?P<confirmation_key>\w+)/$', 'confirm_email', name='confirm_email'),
    url(r'^password_reset/$', 'password_reset', name='password_reset'),
    url(r'^password_reset_confirm/(?P<uidb36>\w+)/(?P<token>[\w\-]+)$', 'password_reset_confirm', name='password_reset_confirm'),
    url(r'^profile/(?P<user_pk>\d+)/$', 'profile', name='profile'),
    url(r'^edit/$', 'edit', name='edit'),
)