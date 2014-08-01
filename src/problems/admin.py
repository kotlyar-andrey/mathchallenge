# -*- coding: utf-8 -*-

from mptt.admin import MPTTModelAdmin
from django.contrib import admin

from . models import Category, Problem, Variant


class CategoryAdmin(MPTTModelAdmin):
    list_display = ('title', 'slug', 'description')
    ordering = ['title']
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 5


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('number', 'category', 'text',)
    list_filter = ('category',)
    ordering = ('category', 'number')
    list_display_links = ('text',)
    inlines = [VariantInline,]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Problem, ProblemAdmin)