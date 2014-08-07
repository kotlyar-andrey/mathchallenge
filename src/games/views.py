# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.template.context import RequestContext

from src.decorators import render_to
from src.games.models import Game
from src.accounts.models import User, GamesResult


@render_to('games/index.html')
def index(request):
    return {'games': Game.objects.all()}


@render_to('games/game.html')
def game(request, game_pk):
    game = get_object_or_404(Game, pk=game_pk)
    all_u = []
    for u in User.objects.all():
        try:
            gb = u.userprogress.games_best.get(game=game)
            all_u.append((u, gb.result))
        except:
            pass
    users = sorted(all_u, key=lambda x: x[::-1], reverse=True)
    return {'game': game, 'users': users}


def game_over(request):
    if request.user.is_authenticated() and request.is_ajax():
        game_pk = request.GET['game_pk']
        points = int(request.GET['points'])
        game = get_object_or_404(Game, pk=game_pk)
        try:
            oldres = request.user.userprogress.games_best.get(game=game)
            if oldres.result < points:
                oldres.result = points
                oldres.save()
        except:
            best_res = GamesResult(game=game, result=points)
            best_res.save()
            request.user.userprogress.games_best.add(best_res)
        return HttpResponse('')
    else:
        return HttpResponse('')



@render_to('games/dev.html')
def dev(requst):
    game = get_object_or_404(Game, pk=1)
    all_u = []
    for u in User.objects.all():
        try:
            gb = u.userprogress.games_best.get(game=game)
            all_u.append((u, gb.result))
        except:
            pass
    users = sorted(all_u, key=lambda x: x[::-1], reverse=True)
    return {'users': users}