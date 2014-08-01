# -*- coding: utf-8 -*-

from mptt.models import MPTTModel, TreeForeignKey
from django.db import models

class Category(MPTTModel):
    title = models.CharField(verbose_name=u'Название категории', max_length=200)
    slug = models.SlugField(verbose_name=u'Ссылка', unique=True)
    description = models.TextField(verbose_name=u'Описание', blank=True)
    sort_number = models.IntegerField(verbose_name=u'Номер по порядку', default=0)
    parent = TreeForeignKey('self', verbose_name=u'Родительская категория',
                            related_name='children', blank=True,
                            help_text=u'Родителеьская категория для данной категории', null=True)

    class MPTTMeta:
        order_insertion_by = ['sort_number']

    class Meta:
        verbose_name = u'Категория задач'
        verbose_name_plural = u'Категории задач'

    def __unicode__(self):
        return self.title


class Problem(models.Model):
    slogn = models.IntegerField(verbose_name=u'Сложность', help_text=u'От 1 до 3', default=1)
    text = models.TextField(verbose_name=u'Текст')
    answer = models.CharField(verbose_name=u'Ответ', max_length=150)
    category = models.ForeignKey(Category, verbose_name=u'Относится к категории')
    klass =  models.IntegerField(verbose_name=u'Класс', blank=True, null=True)
    ist = models.CharField(verbose_name=u'Источник', max_length = 50, blank=True)
    date_add = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(verbose_name=u'Рейтинг задачи', default=0)
    solved = models.IntegerField(verbose_name=u'Количество решивших', default=0)
    number = models.IntegerField(verbose_name=u'Номер задачи', default=0, blank=True)

    class Meta:
        verbose_name = u'Задача'
        verbose_name_plural = u'Задачи'

    def __unicode__(self):
        return self.text[:80]

    @models.permalink
    def get_absolute_url(self):
        return ('problems:problem', (), {'problem_pk': self.pk})

    def inc_solved(self):
        self.solved += 1
        self.save()

    def inc_rating(self):
        self.rating += 1
        self.save()

    def dec_rating(self):
        self.rating -= 1
        self.save()

    def set_number(self, n):
        self.number = n
        self.save()


class Variant(models.Model):
    pro = models.ForeignKey(Problem, verbose_name=u'Задача')
    nam = models.CharField(verbose_name=u'Название', help_text=u'A, B, C, ...', max_length=2)
    val = models.CharField(verbose_name=u'Значение', help_text=u'Строка, число, картинка', max_length=250)
    tru = models.BooleanField(verbose_name=u'Правильный?', default=False)

    class Meta:
        verbose_name = u'Вариант ответа'
        verbose_name_plural = u'Варианты ответов'
        ordering = ('nam',)

    def __unicode__(self):
        return '%s %s' % (self.nam, self.val)