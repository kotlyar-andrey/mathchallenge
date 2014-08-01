# -*- coding: utf-8 -*-

from django.contrib import admin

from . models import Achievment, Check


class AchievmentInline(admin.StackedInline):
    model = Achievment


class CheckAdmin(admin.ModelAdmin):
    inlines = [AchievmentInline,]


admin.site.register(Check, CheckAdmin)