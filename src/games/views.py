# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.template.context import RequestContext

from src.decorators import render_to
from src.games.models import Game


@render_to('games/index.html')
def index(request):
    return {'games': Game.objects.all()}


@render_to('games/game.html')
def game(request, game_pk):
    game = get_object_or_404(Game, pk=game_pk)
    return {'game': game}


@render_to('games/dev.html')
def dev(requst):
    return {}