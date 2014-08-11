# -*- coding: utf-8 -*-

from django import forms
from yacaptcha.fields import YaCaptchaField


class AnswerForm(forms.Form):
    answer = forms.CharField(label=u'Проверить ответ')
    answer.widget.attrs.update({
        'class': 'form-control',
        'placeholder': u'',
    })
    captcha = YaCaptchaField(label=u'Каптча')