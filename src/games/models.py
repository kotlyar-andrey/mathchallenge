# -*- coding: utf-8 -*-

from django.db import models


class Game(models.Model):
    title = models.CharField(verbose_name=u'Название', max_length=200)
    description = models.TextField(verbose_name=u'Описание и правила', help_text=u'Развернуто и с картинками')
    meta_k = models.CharField(verbose_name=u'Ключевые слова', max_length=200, blank=True)
    meta_d = models.CharField(verbose_name=u'Описание', max_length=200, blank=True, help_text=u'Используется на странице игры')
    script_path = models.CharField(verbose_name=u'Путь к js', max_length=200, help_text=u'/static/js/games/game.js', blank=True)
    style_path = models.CharField(verbose_name=u'Путь к css', max_length=200, help_text=u'/static/css/games/game.css', blank=True)
    content = models.TextField(verbose_name=u'Содержимое страницы, разметка')
    rating = models.IntegerField(verbose_name=u'Рейтинг игры', default=0)

    class Meta:
        verbose_name = u'Игра'
        verbose_name_plural = u'Игры'

    def __unicode__(self):
        return self.title