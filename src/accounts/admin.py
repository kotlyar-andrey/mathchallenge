# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .forms import AdminUserAddForm, AdminUserChangeForm
from .models import User, UserProgress, ChallengeResult


class ProgressInline(admin.StackedInline):
    model = UserProgress


class UserAdmin(admin.ModelAdmin):
    inlines = [ProgressInline,]
    form = AdminUserChangeForm
    add_form = AdminUserAddForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_valid_email')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'email',
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )


class ChallengeResultAdmin(admin.ModelAdmin):
    list_display = ('category', 'result',)
    list_filter = ('category',)
    ordering = ('category', 'result')
    list_display_links = ('category',)
#
# class UserAdmin(admin.ModelAdmin):
#     form = AdminUserChangeForm
#     add_form = AdminUserAddForm
#     fieldsets = (
#         (None, {'fields': ('username', 'password',)}),
#         (_('Personal info'), {'fields': (
#             'first_name',
#             'last_name',
#             'email',
#         )}),
#         (u'Прогресс', {'fields': ('progress',)}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2')}
#         ),
#     )


admin.site.register(User, UserAdmin)
admin.site.register(UserProgress)
admin.site.register(ChallengeResult, ChallengeResultAdmin)