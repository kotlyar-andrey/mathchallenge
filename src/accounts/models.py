# -*- coding: utf-8 -*-

import hashlib
import random
import os
import re
from datetime import timedelta

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core import validators
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from src.mail import send_templated_email
from src.lessons.models import Theme, Lesson, Task
from src.problems.models import Problem, Category
from src.achievments.models import Achievment
from src.games.models import Game


EMAIL_CONFIRMATION_DAYS = getattr(settings, 'EMAIL_CONFIRMATION_DAYS', 3)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        user = self.model(
            username=username,
            is_staff=False, is_active=True, is_superuser=False,
            )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters'),
                                validators=[
                                    validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
                                ])
    email = models.EmailField(
        verbose_name=u'Электронная почта',
        max_length=250,
        unique=True,
        db_index=True,
        blank=True, null=True
    )
    is_valid_email = models.BooleanField(_(u'Правильная электронная почта?'), default=False)
    first_name = models.CharField(u'Имя', max_length=30, blank=True)
    last_name = models.CharField(u'Фамилия', max_length=30, blank=True)
    date_joined = models.DateTimeField(u'Дата регистрации', default=timezone.now)
    favorite_problems = models.ManyToManyField(Problem, verbose_name=u'Избранные задачи',
                                               related_name='fav', blank=True, null=True)
    ratings_problems = models.ManyToManyField(Problem, verbose_name=u'Оцененные задачи',
                                              related_name='rat', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'

    def save(self, *args, **kwargs):
        send_confirmation = False

        if not self.email:
            self.is_valid_email = False
        elif self.pk:
            try:
                before_save = self.__class__._default_manager.get(pk=self.pk)
                send_confirmation = before_save.email != self.email
            except models.ObjectDoesNotExist:
                send_confirmation = True
        elif not self.is_valid_email:
            send_confirmation = True

        if send_confirmation:
            self.is_valid_email = False

        send_email_confirmation = kwargs.pop('send_email_confirmation', True)
        super(User, self).save(*args, **kwargs)

        if send_confirmation and send_email_confirmation:
            EmailConfirmation.objects.send_confirmation(self)

    def get_full_name(self):
        # The user is identified by their email address
        return '%s %s' % (self.first_name, self.last_name) if self.first_name or self.last_name else self.username

    def get_email(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.username

    def get_username(self):
        return self.username

    def gravatar_photo(self):
        return 'http://www.gravatar.com/avatar/%s.jpg?d=wavatar' % self.getMD5()

    def avatar(self):
        return self.gravatar_photo()

    def getMD5(self):
        m = hashlib.md5()
        m.update(self.email or self.username + '@mathchallenge.ru')
        return m.hexdigest()

    @property
    def get_points(self):
        count = 0
        for pr in self.userprogress.problems_solved_problems.all():
            if pr.category in Category.objects.get(slug='kenguru').get_children() or pr.category in Category.objects.get(slug='olimpiada').get_children():
                if pr.slogn == 1:
                    count += 3
                elif pr.slogn == 2:
                    count += 4
                elif pr.slogn ==3:
                    count += 5
            else:
                count += 5
        return count


class ChallengeResult(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'Категория')
    result = models.IntegerField(verbose_name=u'Лучший результат')

    class Meta:
        verbose_name = u'Лучший результат испытания'
        verbose_name_plural = u'Лучшие результаты испытаний'


    def __unicode__(self):
        return u'%s - %s' % (self.category, self.result)


class GamesResult(models.Model):
    game = models.ForeignKey(Game, verbose_name=u'Игра')
    result = models.IntegerField(verbose_name=u'Лучший результат')

    class Meta:
        verbose_name = u'Лучший результат игры'
        verbose_name_plural = u'Лучшие результаты игр'


    def __unicode__(self):
        return u'%s - %s' % (self.game, self.result)


class UserProgress(models.Model):
    user = models.OneToOneField(User, verbose_name=u'Пользователь')
    lessons_solved_tasks = models.ManyToManyField(
        Task,
        verbose_name=u'Решенные задачи уроков',
        related_name=u'lessons_solved_task',
        blank=True, null=True,default=None
    )
    lessons_solved_lessons = models.ManyToManyField(
        Lesson,
        verbose_name=u'Пройденные уроки',
        related_name=u'lessons_solved_lesson',
        blank=True, null=True, default=None
    )
    lessons_solved_themes = models.ManyToManyField(
        Theme,
        verbose_name=u'Пройденные темы',
        related_name=u'lessons_solved_theme',
        blank=True,null=True, default=None
    )
    problems_solved_problems = models.ManyToManyField(
        Problem,
        verbose_name=u'Решенные задачи',
        related_name=u'problems_solved_problem',
        blank=True, null=True, default=None
    )
    achievments = models.ManyToManyField(
        Achievment,
        verbose_name=u'Полученные достижения',
        related_name=u'achievments',
        blank=True, null=True, default=None
    )
    challenge_best = models.ManyToManyField(
        ChallengeResult,
        verbose_name=u'Лучшие результаты испытаний',
        blank=True, null=True,default=None
    )
    games_best = models.ManyToManyField(
        GamesResult,
        verbose_name=u'Лучшие результаты игр',
        blank=True, null=True, default=None
    )

    def __unicode__(self):
        return self.user.get_full_name() + ' progress'


def create_progress(sender, **kwargs):
    if kwargs['created']:
        UserProgress.objects.create(user=kwargs['instance'])
models.signals.post_save.connect(create_progress, sender=User)


class EmailConfirmationManager(models.Manager):

    def confirm_email(self, confirmation_key):
        try:
            confirmation = self.get(confirmation_key=confirmation_key)
        except self.model.DoesNotExist:
            return None
        if not confirmation.key_expired():
            user = confirmation.user
            user.is_valid_email = True
            user.save()
            return user

    def send_confirmation(self, user):
        assert user.email
        self.filter(user=user).delete()
        salt = hashlib.sha224(str(random.random()) + settings.SECRET_KEY).hexdigest()[:5]
        confirmation_key = hashlib.sha224(salt + user.email).hexdigest()[:39]
        try:
            current_site = Site.objects.get_current()
        except Site.DoesNotExist:
            return
        path = reverse("accounts:confirm_email", args=[confirmation_key])
        activate_url = u"http://%s%s" % (unicode(current_site.domain), path)
        context = {
            "user": user,
            "activate_url": activate_url,
            "current_site": current_site,
            "confirmation_key": confirmation_key,
            }
        subject = _(u'Please confirm your email address for %(site)s') % {'site': current_site.name}
        send_templated_email(user.email, subject, 'accounts/email_confirmation_message.html', context, fail_silently=settings.DEBUG)
        return self.create(
            user=user,
            sent=timezone.now(),
            confirmation_key=confirmation_key)

    def delete_expired_confirmations(self):
        d = timezone.now() - timedelta(days=EMAIL_CONFIRMATION_DAYS)
        self.filter(sent__lt=d).delete()


class EmailConfirmation(models.Model):
    user = models.ForeignKey(User)
    sent = models.DateTimeField()
    confirmation_key = models.CharField(max_length=40)

    objects = EmailConfirmationManager()

    def __unicode__(self):
        return u"confirmation for %s" % self.user.email

    class Meta:
        verbose_name = _("e-mail confirmation")
        verbose_name_plural = _("e-mail confirmations")

    def key_expired(self):
        expiration_date = self.sent + timedelta(days=EMAIL_CONFIRMATION_DAYS)
        return expiration_date <= timezone.now()
    key_expired.boolean = True
