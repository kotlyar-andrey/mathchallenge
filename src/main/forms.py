# -*- coding: utf-8 -*-

from django import forms
from django.core.mail import EmailMessage
from django.utils import timezone

from yacaptcha.fields import YaCaptchaField
from src import settings


class FeedbackForm(forms.Form):
    name = forms.CharField(label=u'Имя')
    email = forms.EmailField(label=u'Email', required=False, help_text=u'не обязательно')
    message = forms.CharField(label=u'Сообщение', widget=forms.Textarea())
    referer = forms.CharField(required=False, widget=forms.HiddenInput())
    captcha = YaCaptchaField(label=u'Введите символы с картинки')

    def send(self, request):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        user_agent_data = 'User agent: %s' % request.META.get('HTTP_USER_AGENT')
        timestamp = 'Time: %s' % timezone.now().strftime('%H:%M:%S %m-%d-%Y')
        referer = 'Referer: %s' % self.cleaned_data['referer']
        message = '%s\n%s\n\n%s\n%s\n%s' % (name, message, user_agent_data, timestamp, referer)
        headers = {'Reply-To': email} if email else None

        EmailMessage(settings.FEEDBACK_SUBJECT, message, email, [a[1] for a in settings.ADMINS], headers=headers).send()
