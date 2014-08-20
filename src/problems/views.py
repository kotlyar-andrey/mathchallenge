# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from src.decorators import render_to, paginators
from . models import Category, Problem
from . forms import AnswerForm
from src.accounts.models import User

@render_to('problems/index.html')
def index(request):
    last_pr = Problem.objects.all().order_by('-date_add')[:5]
    rating_pr = Problem.objects.all().order_by('-rating')[:5]
    return locals()


@render_to('problems/category.html')
def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    problem_list = category.problem_set.all().order_by('number')
    return {'category': category, 'problems': paginators(request, problem_list, 15)}


def get_prew_next_problem(pr):
    all_cat_pr = list(Problem.objects.filter(category=pr.category).order_by('number'))
    ind = all_cat_pr.index(pr)
    prw, nxt = (0, 0)
    if ind > 0:
        prw = all_cat_pr[ind - 1]
    if ind < len(all_cat_pr) - 1:
        nxt = all_cat_pr[ind + 1]
    return (prw, nxt)


def change_rating(request, pr):
    if 'plus' in request.POST.keys():
        #Если нажата кнопка увеличения рейтинга
        if not pr in request.user.ratings_problems.all():
            request.user.ratings_problems.add(pr)
            pr.inc_rating()
            messages.success(request, u'Спасибо за оценку.')
        else:
            messages.error(request, u'Ошибка. Вы уже оценили эту задачу.')
    elif 'minus' in request.POST.keys():
        #Если нажата кнопка уменьшения рейтинга
        if not pr in request.user.ratings_problems.all():
            request.user.ratings_problems.add(pr)
            pr.dec_rating()
            messages.success(request, u'Спасибо за оценку.')
        else:
            messages.error(request, u'Ошибка. Вы уже оценили эту задачу.')


@render_to('problems/problem.html')
def problem(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    prw, nxt = get_prew_next_problem(problem)
    form = AnswerForm()
    if request.method == 'POST':
        #Произошла отправка ответа или изменение рейтинга
        if request.user.is_authenticated():
            change_rating(request, problem)
        if 'answ' in request.POST.keys():
            form = AnswerForm(request.POST)
            if form.is_valid():
                otv = request.POST['answer']
                if otv == problem.answer:
                    messages.success(request, u'Ответ верный!')
                    if request.user.is_authenticated() and not problem in request.user.userprogress.problems_solved_problems.all():
                        problem.inc_solved()
                        request.user.userprogress.problems_solved_problems.add(problem)
                    return HttpResponseRedirect(problem.get_absolute_url())
                else:
                    messages.error(request, u'Ответ не верный.')
            else:
                messages.error(request, u'Символы с картинки введены не правильно.')
    return {'problem': problem, 'prw': prw, 'nxt': nxt, 'form': form}


@login_required
def add_fav(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)
    ref = request.META.get('HTTP_REFERER', '/')
    if problem in request.user.favorite_problems.all():
        request.user.favorite_problems.remove(problem)
        messages.success(request, u'Задача удалена с избранного.')
    else:
        request.user.favorite_problems.add(problem)
        messages.success(request, u'Задача добавлена в избранное.')
    return HttpResponseRedirect(ref)



def pr_numbering(request):
    if request.user.username == 'kotlyar':
        all_cat = Category.objects.all()
        for category in all_cat:
            if not category.parent: continue
            i = 1
            for pr in category.problem_set.all().order_by('slogn'):
                pr.set_number(i)
                i = i + 1
    else:
        raise Http404
    return HttpResponseRedirect('/')


@render_to('problems/error_test.html')
def error_test(request):
    error_problems = []
    if request.user.username == 'kotlyar':
        keng_cat = Category.objects.get(slug='kenguru').get_children()
        for cat in keng_cat:
            for pr in cat.problem_set.all():
                check = False
                for variant in pr.variant_set.all():
                    if variant.tru:
                        check = True
                        if not pr.answer in variant.val:
                            error_problems.append(pr)
                        break
                if not check:
                    error_problems.append(pr)
    return {'error_problems': error_problems}


@render_to('problems/board.html')
def board(request):
    all_u = User.objects.all()
    users = sorted([(u, u.get_points) for u in all_u], key=lambda x: x[::-1], reverse=True)
    us = [u[0] for u in users]
    return {'users': us}