# -*- coding: utf-8 -*-

from django.template import Library
from src.achievments.models import Achievment

register = Library()


@register.inclusion_tag('achievments/_achievment.html')
def achievment(pk):
    try:
        ach = Achievment.objects.get(pk=pk)
    except:
        ach = ''
    return {'achievment': ach}