# -*- coding: utf-8 -*-

from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import password_reset as auth_password_reset, password_reset_confirm as auth_password_reset_confirm
from django.contrib.auth.decorators import login_required

from src.decorators import render_to, to_list
from .forms import CreateUserForm, PasswordResetForm, UserEditForm
from .models import User, EmailConfirmation
from src.problems.models import Category, Problem
from src.lessons.models import Theme
from src.achievments.models import Achievment


@render_to('accounts/create.html')
def create(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'Учетная запись создана! На указанный почтовый адрес отправлено письмо с подтверждением. Пожалуйста, проверьте почту.')
            return redirect('accounts:login')
        messages.error(request, u'Пожалуйста, исправьте ошибки и отправьте форму еще раз.')
    else:
        form = CreateUserForm()
    return {
        'form': form
    }


def logout(request):
    from django.contrib.auth import logout
    logout(request)
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '/')
    return redirect(redirect_to)


def confirm_email(request, confirmation_key):
    confirmation_key = confirmation_key.lower()
    user = EmailConfirmation.objects.confirm_email(confirmation_key)

    if not user:
        messages.error(request, u'Ссылка с кодом подтверждения не действительна.')
        return redirect('/')
    else:
        messages.success(request, u'Электронная почта подтверждена.')
        return redirect('/auth/login/')


def password_reset(request):
    response = auth_password_reset(request,
                                   template_name='accounts/password_reset.html',
                                   email_template_name='accounts/password_reset_email.html',
                                   password_reset_form=PasswordResetForm,
                                   post_reset_redirect='/')

    if isinstance(response, HttpResponseRedirect):
        messages.success(request, u'На Ваш адрес электронной почты отправлено письмо с инструкцией по изменению пароля.')
        return response

    return response


def password_reset_confirm(request, uidb36, token):
    return auth_password_reset_confirm(request, uidb36, token,
                                       post_reset_redirect=reverse('accounts:password_reset_complete'),
                                       template_name='accounts/password_reset_confirm.html'
    )


@render_to('accounts/profile.html')
def profile(request, user_pk):
    user_obj = get_object_or_404(User, pk=user_pk)

    # Задачи
    all_cat = Category.objects.all()
    categories = []
    for category in all_cat:
        if category.parent: continue
        categories.append([category, to_list(category.get_children(), 3)])
    solved_progress = int(float(len(user_obj.userprogress.problems_solved_problems.all())) / float(len(Problem.objects.all())) * 100)

    #Уроки
    themes = [[i + 5, Theme.objects.filter(klass=(i+5))] for i in range(7)]

    #Испытания
    chall_cat = [cb.category for cb in user_obj.userprogress.challenge_best.all()]

    #Избранное
    favorite_problems = user_obj.favorite_problems.all()

    #Достижения
    achievments = Achievment.objects.all()

    return {'categories': categories, 'user_obj': user_obj, 'solved_progress': solved_progress, 'pr_count': len(Problem.objects.all()),
            'themes': themes,
            'chall_cat': chall_cat,
            'favorites': favorite_problems,
            'achievments': achievments,}


@render_to('accounts/edit.html')
@login_required
def edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, u'Профиль успешно сохранен! Подтвердите адрес электронной почты, если он был изменен.')
            return redirect('accounts:profile', request.user.pk)
        messages.error(request, u'Пожалуйста, исправьте ошибки.')
    else:
        form = UserEditForm(instance=request.user)
    return {'form': form}