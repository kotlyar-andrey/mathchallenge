# -*- coding: utf-8 -*-


import random
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from src.decorators import render_to
from src.problems.models import Category, Problem, Variant
from src.accounts.models import ChallengeResult


@render_to('challenge/index.html')
def index(request):
    categories = ''
    if 'challenge' in request.GET.keys() and (request.GET['challenge']=='kenguru' or request.GET['challenge']=='olimpiada'):
        ch = get_object_or_404(Category, slug=request.GET['challenge'])
        if 'category' in request.GET.keys() and not (request.GET['category']=='kenguru' or request.GET['category']=='olimpiada'):
            #выбраны категории, запускаем испытание
            cat = get_object_or_404(Category, slug=request.GET['category'])
            return HttpResponseRedirect(reverse('challenges:challenge', args=(cat.slug,)))
        else:
            categories = ch.get_children()
    return {'categories': categories}


def challenge_change(request):
    if request.is_ajax() and request.method == "GET" and 'challenge' in request.GET.keys():
        challenge = request.GET['challenge']
        categories = get_object_or_404(Category, slug=challenge).get_children()
        return render_to_response('challenge/_category_select.html',
                                  {'categories': categories},
                                  )
    else:
        raise Http404


def get_randoms(objects, count):
    res = []
    for i in range(count):
        obj = random.choice(objects)
        objects.remove(obj)
        res.append(obj)
    return res


def challenge(request, category_slug):
    cat = get_object_or_404(Category, slug=category_slug)
    problems1, problems2, problems3 = (list(cat.problem_set.all().filter(slogn=1)), list(cat.problem_set.all().filter(slogn=2)), list(cat.problem_set.all().filter(slogn=3)))
    if cat.parent.slug == 'kenguru':
        if cat.slug == 'malysh_2' or cat.slug == 'malysh_34':
            problems = get_randoms(problems1, 10)+get_randoms(problems2, 10)+get_randoms(problems3, 5)
        else:
            problems = get_randoms(problems1, 10)+get_randoms(problems2, 10)+get_randoms(problems3, 10)
        return render_to_response('challenge/kenguru.html', {'problems':problems, 'category':cat}, context_instance=RequestContext(request))
    elif cat.parent.slug == 'olimpiada':
        problems = get_randoms(problems1, 2)+get_randoms(problems2, 2)+get_randoms(problems3, 1)
        return render_to_response('challenge/olimpiada.html', {'problems':problems, 'category':cat}, context_instance=RequestContext(request))
    else:
        raise Http404


def kenguru_check(request):
    if request.is_ajax():
        true_count, true_3, true_4, true_5, ball, true_problems, cb_result = (0, 0, 0, 0, 0, [], '')
        for k in request.POST.keys():
            if k == 'csrfmiddlewaretoken': continue
            answer = get_object_or_404(Variant, pk=int(request.POST[k]))
            if answer.tru:
                true_problems.append(answer.pro.pk)
                true_count += 1
                if answer.pro.slogn == 1:
                    true_3 += 1
                    ball += 3
                elif answer.pro.slogn == 2:
                    true_4 += 1
                    ball += 4
                elif answer.pro.slogn == 3:
                    true_5 += 1
                    ball += 5
            cat = answer.pro.category.slug
        if request.user.is_authenticated():
            category = get_object_or_404(Category, slug=cat)
            for cb in request.user.userprogress.challenge_best.all():
                if category == cb.category:
                    cb_result = cb.result
                    break
            try:
                oldres = request.user.userprogress.challenge_best.get(category=category)
                if oldres.result < ball:
                    oldres.result = ball
                    oldres.save()
            except:
                bestres = ChallengeResult(category=category,result=ball)
                bestres.save()
                request.user.userprogress.challenge_best.add(bestres)
        return render_to_response('challenge/_kenguru_res.html', {'true_count': true_count,
                                                                  'true_3': true_3,
                                                                  'true_4': true_4,
                                                                  'true_5': true_5,
                                                                  'ball': ball,
                                                                  'true_problems': true_problems,
                                                                  'cat': cat,
                                                                  'cb_result': cb_result})
    else:
        raise Http404

