# -*- coding: utf-8

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('social_auth.urls')),
    url(r'^', include('src.main.urls', 'main')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lessons/', include('src.lessons.urls', 'lessons')),
    url(r'^problems/', include('src.problems.urls', 'problems')),
    url(r'^auth/', include('src.accounts.urls', 'accounts')),
    url(r'^achievments/', include('src.achievments.urls', 'achievments')),
    url(r'^challenge/', include('src.challenge.urls', 'challenges')),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)