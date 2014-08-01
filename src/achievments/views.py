# -*- coding: utf-8 -*-

from django.http import Http404
from src.decorators import render_to
from . models import Achievment


@render_to('achievments/index.html')
def index(request):
    ach = Achievment.objects.all()
    return {'achievments': ach}


# def challenge_change(request):
#     if request.is_ajax() and request.method == "GET":
#         data = []
#         all_ach = Achievment.objects.all()
#         for ach in all_ach:
#             if not ach in request.user.userprogress.achievments.all() and ach.check.test_a(request.user):
#                 request.user.userprogress.achievments.add(ach)
#                 data.append(ach)
#         return render_to_response('main/_achievment.html',
#                                   {'achievments': data},
#                                   context_instance=RequestContext(request))
#     else:
#         raise Http404