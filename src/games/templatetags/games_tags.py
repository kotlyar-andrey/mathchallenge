# -*- coding: utf-8

from django.template import Library
from django.shortcuts import get_object_or_404

from src.accounts.models import User
from src.games.models import Game

register = Library()


@register.inclusion_tag('games/_results.html', takes_context=True)
def inc_res(context, game_pk):
    game = get_object_or_404(Game, pk=game_pk)
    all_u = []
    for u in User.objects.all():
        try:
            gb = u.userprogress.games_best.get(game=game)
            all_u.append((u, gb.result))
        except:
            pass
    users = sorted(all_u, key=lambda x: x[::-1], reverse=True)
    return {'users': users, 'user': context['user']}