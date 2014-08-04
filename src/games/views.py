# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.template.context import RequestContext

from src.decorators import render_to


@render_to('games/index.html')
def index(request):
    return {}