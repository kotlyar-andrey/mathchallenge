# -*- coding: utf-8 -*-

from django.template import Library
from src.problems.models import Category
from src.decorators import to_list

register = Library()

@register.inclusion_tag('problems/_sidebar.html', takes_context=True)
def sidebar(context):
    all_cat = Category.objects.all()
    categories = []
    for category in all_cat:
        if category.parent: continue
        categories.append([category, category.get_children()])
    if 'category' in context:
        active_cat = context['category']
    else:
        active_cat = ''
    return {'cat': categories, 'active_cat': active_cat}


@register.inclusion_tag('problems/_pr_tables.html', takes_context=True)
def tables(context, objects):
    rows = to_list(objects.order_by('number'), 10)
    return {'rows': rows, 'user': context['user']}


@register.filter()
def index_of(obj, l):
    return l.index(obj)


@register.filter()
def backgroung_slogn(value):
    if value == 1:
        return 'slogn1'
    elif value == 2:
        return 'slogn2'
    elif value == 3:
        return 'slogn3'
    else:
        return