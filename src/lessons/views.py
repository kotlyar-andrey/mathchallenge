# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from src.decorators import render_to
from . models import Theme, Task, Lesson
from . forms import AnswerForm


@render_to('lessons/index.html')
def index(request):
    themes = [[i + 5, Theme.objects.filter(klass=(i+5))] for i in range(7)]
    return {'themes': themes,}


@render_to('lessons/theme.html')
def theme(request, theme_pk):
    theme = get_object_or_404(Theme, pk=theme_pk)
    return {'theme': theme}


@render_to('lessons/lesson.html')
def lesson(request, theme_pk, lesson_number):
    form = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
    theme = get_object_or_404(Theme, pk=theme_pk)
    lesson_count = len(theme.lesson_set.all())
    try:
        lesson = theme.lesson_set.get(number=lesson_number)
    except:
        lesson = theme.lesson_set.all().order_by('number')[lesson_count-1]
    tasks = lesson.task_set.all().order_by('slog')
    return {'theme': theme, 'lesson': lesson, 'tasks': tasks, 'form': form}


def answer_check(request):
    if request.is_ajax() and request.method == "POST":
        data = False
        task_pk = request.POST['task_pk']
        ans = request.POST['answer']
        task = get_object_or_404(Task, pk=task_pk)
        if ans == task.answer:
            data = True
            if request.user.is_authenticated():
                request.user.userprogress.lessons_solved_tasks.add(task)

                less = task.lesson
                lesson_complit = True
                for t in less.task_set.all():
                    if not t in request.user.userprogress.lessons_solved_tasks.all():
                        lesson_complit = False
                        break
                if lesson_complit:
                    request.user.userprogress.lessons_solved_lessons.add(less)
                    th = less.theme
                    theme_complit = True
                    request.user.userprogress.lessons_solved_tasks = ''
                    for l in th.lesson_set.all():
                        if not l in request.user.userprogress.lessons_solved_lessons.all():
                            theme_complit = False
                            break
                    if theme_complit:
                        request.user.userprogress.lessons_solved_themes.add(th)
                        data = 'theme_complit'
        return HttpResponse(data)
    else:
        raise Http404
