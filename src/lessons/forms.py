# -*- coding: utf-8 -*-

from django import forms

from . models import Task


class AnswerForm(forms.Form):
    answer = forms.CharField()
    answer.widget.attrs.update({
        'class': 'form-control',
        'placeholder': u'Ответ',
        'onkeydown': "javascript:if(13==event.keyCode){return false;}"
    })