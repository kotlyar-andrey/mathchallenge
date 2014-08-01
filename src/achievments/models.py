# -*- coding: utf-8 -*-

from django.db import models


class Check(models.Model):
    test_code = models.TextField(verbose_name=u'Функция проверки')

    class Meta:
        verbose_name = u'Достижение'
        verbose_name_plural = u'Достижения'

    def __unicode__(self):
        return self.achievment.title

    def test_a(self, user):
        result = False
        exec self.test_code
        return  result

class Achievment(models.Model):
    title = models.CharField(verbose_name=u'Название', max_length=250)
    image = models.ImageField(verbose_name=u'Изображение', upload_to='achievments/', help_text=u'Спрайт на активную и неактивную  версию', blank=True, null=True)
    sort_number = models.IntegerField(verbose_name=u'Номер по списку', blank=True, null=True)
    condition = models.CharField(verbose_name=u'Условие выполнения', max_length=250)
    check = models.OneToOneField(Check, verbose_name=u'Функция проверки')

    class Meta:
        verbose_name = u'Описание достижения'
        verbose_name_plural = u'Описание достижений'
        ordering = ('sort_number', 'title')

    def __unicode__(self):
        return self.title
