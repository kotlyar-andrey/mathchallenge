# -*- coding: utf-8 -*-

from django.template import Library

register = Library()


@register.filter()
def slog_color(value):
    if value == 1:
        return 'green'
    elif value == 2:
        return 'yellow'
    elif value == 3:
        return 'red'
    elif value == 4:
        return 'aqua'
    else:
        return 'grey'


@register.filter()
def get_theme_progress(user, theme):
    all_lessons = len(theme.lesson_set.all())
    solved_lessons = 0
    for lesson in theme.lesson_set.all():
        if lesson in user.userprogress.lessons_solved_lessons.all():
            solved_lessons += 1
    return int(float(solved_lessons) / float(all_lessons) * 100)

@register.filter()
def get_lesson_progress(user, theme):
    solved_lessons = 0
    for lesson in theme.lesson_set.all():
        if lesson in user.userprogress.lessons_solved_lessons.all():
            solved_lessons += 1
    return solved_lessons