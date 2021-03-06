# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib import messages

from src.decorators import render_to
from src.achievments.models import Achievment
from src.accounts.models import User
from src.problems.models import Problem
from . forms import FeedbackForm


@render_to('main/index.html')
def index(request):
    users = User.objects.all()
    solved_problems = 0
    achievments = 0
    for u in users:
        solved_problems += len(u.userprogress.problems_solved_problems.all())
        achievments += len(u.userprogress.achievments.all())
    return {
        'user_count': len(users),
        'solved_count': solved_problems,
        'ach_done_count': achievments,
        'problems_count': len(Problem.objects.all()),

    }


def achievments_check(request):
    if request.is_ajax() and request.method == "GET" and request.user.is_authenticated():
        data = []
        all_ach = Achievment.objects.all()
        for ach in all_ach:
            if not ach in request.user.userprogress.achievments.all() and ach.check.test_a(request.user):
                request.user.userprogress.achievments.add(ach)
                data.append(ach)
        return render_to_response('main/_achievment.html',
                                  {'achievments': data},
                                  context_instance=RequestContext(request))
    else:
        raise Http404


@render_to('main/feedback.html')
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.send(request)
            messages.success(request, u'Сообщение отправлено, спасибо.')
            return redirect('main:feedback')
    else:
        form = FeedbackForm(initial={'reerer': request.META.get('HTTP_REFERER', '')})
    return {'form': form}
