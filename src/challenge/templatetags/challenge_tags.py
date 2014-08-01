# -*- coding: utf-8 -*-

from django.template import Library

register = Library()


@register.filter()
def kenguru_result(value,slug):
    if value < 20:
        return 'red-color'
    elif value >= 20 and value < 80:
        return 'blue-color'
    elif value >= 80:
        if (value == 95 and (slug == 'malysh_2' or slug == 'malysh_34')) or value == 120:
            return 'fa fa-star-o gold-color'
        else:
            return 'green-color'