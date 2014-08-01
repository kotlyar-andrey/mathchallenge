# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def render_to(template, processor=None):
    def renderer(func):
        def wrapper(request, *args, **kw):
            if processor is not None:
                ctx_proc = RequestContext(request, processors=[processor])
            else:
                ctx_proc = RequestContext(request)
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], ctx_proc)
            elif isinstance(output, dict):
                return render_to_response(template, output, ctx_proc)
            return output
        return wrapper
    return renderer


def paginators(request, objects, count=20):
    paginator = Paginator(objects, count)
    page = request.GET.get('page')
    try:
        mass = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        mass = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        mass = paginator.page(paginator.num_pages)
    return mass


def to_list(l,n):
    """
    Возвращает список обектов l в виде списка списков, в которых объекты по n штук
    """
    row_c = (len(l) // n + 1) if len(l) % n else len(l) // n
    a = []
    for i in range(row_c):
        a.append(l[n*i:n*(i+1)])
    return a