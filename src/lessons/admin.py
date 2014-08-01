# -*- coding: utf-8 -*-

from django.contrib import admin

from . models import Theme, Lesson, Task, Remember

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

class RememberInline(admin.TabularInline):
    model = Remember
    extra = 1

class LessonAdmin(admin.ModelAdmin):
    inlines = [TaskInline, RememberInline]
    list_display = ('title', 'theme', 'number')
    ordering = ('theme', 'number')
    list_filter = ('theme',)
    model = Lesson


    class Media:
        js = [
            '/static/js/jquery-1.8.2.min.js',
            '/static/ckeditor/ckeditor.js',
            # '/static/ckeditor/adapters/jquery.js',
            '/static/ckeditor/cke_init.js',
        ]

class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'sort_number', 'klass')
    ordering = ('klass', 'sort_number',)

admin.site.register(Theme, ThemeAdmin)
admin.site.register(Lesson, LessonAdmin)