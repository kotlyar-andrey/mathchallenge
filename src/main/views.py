# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from src.decorators import render_to
from src.achievments.models import Achievment


@render_to('main/index.html')
def index(request):
    return {'achs': Achievment.objects.all()}


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
