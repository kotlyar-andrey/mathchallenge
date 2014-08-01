# -*- coding: utf-8 -*-

from django.db import models


class Theme(models.Model):
    title = models.CharField(verbose_name=u'Название темы', max_length=150)
    description = models.TextField(verbose_name=u'Описание', blank=True)
    klass = models.IntegerField(verbose_name=u'Класс')
    sort_number = models.IntegerField(u'Номер темы по списку')
    complit_count = models.IntegerField(u'Количество прошедших', default=0)

    class Meta:
        verbose_name = u'Тема'
        verbose_name_plural = u'Темы'

    def __unicode__(self):
        return self.title


class Lesson(models.Model):
    theme = models.ForeignKey(Theme, verbose_name=u'Тема')
    number = models.IntegerField(verbose_name=u'Номер урока')
    title = models.CharField(verbose_name=u'Название', max_length=150)
    material = models.TextField(verbose_name=u'Учебный материал')
    test = models.BooleanField(verbose_name=u'Контрольная работа', default=False)


    class Meta:
        verbose_name = u'Урок'
        verbose_name_plural = u'Уроки'

    def __unicode__(self):
        return self.title


class Task(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'Урок')
    text = models.TextField(verbose_name=u'Текст задания')
    answer = models.CharField(verbose_name=u'Ответ', max_length=150)
    slog = models.IntegerField(verbose_name=u'Сложность',
                               help_text=u'От 1 до 3', default='1')

    class Meta:
        verbose_name = u'Задание'
        verbose_name_plural = u'Задания'

    def __unicode__(self):
        return self.text[:20]


class Remember(models.Model):
    title = models.CharField(verbose_name=u'Заголовок', max_length=150, blank=True)
    text =models.TextField(verbose_name=u'Текст')
    lesson = models.ForeignKey(Lesson, verbose_name=u'К уроку...')

    class Meta:
        verbose_name = u'Запоминалка'
        verbose_name_plural = u'Запоминалки'

    def __unicode__(self):
        return self.title
