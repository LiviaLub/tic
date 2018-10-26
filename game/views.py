from random import randint

from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Game, Move


def index(request):
    context = {}
    data = {
        '00': 'click',
        '01': 'click',
        '02': 'click',
        '10': 'click',
        '11': 'click',
        '12': 'click',
        '20': 'click',
        '21': 'click',
        '22': 'click',
    }
    game = Game.objects.filter().last()
    game_id = game.id
    for move in Move.objects.filter(game_id=game_id):
        coordinate = '{}{}'.format(move.coordinate_x, move.coordinate_y)
        data[coordinate] = move.player
    context['data'] = data
    context['winner'] = game.winner if game.winner else None
    return render(request, "game/game_board.html", context)


def move(request, x, y):
    game_id = Game.objects.filter(winner__isnull=True).last().id
    if not Move.objects.filter(coordinate_x=x, coordinate_y=y, game_id=game_id).exists():
        x_moved = True
        move_x = Move(player='x', coordinate_x=x, coordinate_y=y, game_id=game_id)
        move_x.save()
        is_winner = check_winner('x', game_id)
        if is_winner:
            return HttpResponseRedirect('/game')
        free = False
        while not free:
            move_o_x = randint(0, 2)
            move_o_y = randint(0, 2)
            if not Move.objects.filter(coordinate_x=move_o_x, coordinate_y=move_o_y, game_id=game_id).exists():
                move_o = Move(player='o', coordinate_x=move_o_x, coordinate_y=move_o_y, game_id=game_id)
                move_o.save()
                is_winner = check_winner('o', game_id)
                if is_winner:
                    return HttpResponseRedirect('/game')
                free = True
    else:
        x_moved = False
    return HttpResponseRedirect('/game')


def check_winner(player, game_id):
    game = Game.objects.get(pk=game_id)
    x_moves = list(Move.objects.filter(player=player, game_id=game_id).values('coordinate_x').annotate(total=Count('coordinate_x')))
    for item in x_moves:
        if item['total'] == 3:
            game.winner = player
            game.save()
            return True
    y_moves = list(Move.objects.filter(player=player, game_id=game_id).values('coordinate_y').annotate(total=Count('coordinate_y')))
    for item in y_moves:
        if item['total'] == 3:
            game.winner = player
            game.save()
            return True
    move_00 = Move.objects.filter(player=player, coordinate_x=0, coordinate_y=0, game_id=game_id).exists()
    move_11 = Move.objects.filter(player=player, coordinate_x=1, coordinate_y=1, game_id=game_id).exists()
    move_22 = Move.objects.filter(player=player, coordinate_x=2, coordinate_y=2, game_id=game_id).exists()
    move_02 = Move.objects.filter(player=player, coordinate_x=0, coordinate_y=2, game_id=game_id).exists()
    move_20 = Move.objects.filter(player=player, coordinate_x=2, coordinate_y=0, game_id=game_id).exists()
    if (move_00 and move_11 and move_22) or (move_02 and move_11 and move_20):
        game = Game.objects.get(pk=game_id)
        game.winner = player
        game.save()
        return True
    move_count = Move.objects.filter(game_id=game_id).count()
    if move_count == 9:
        game.winner = "T"
        game.save()
    return False


def new_game(request):
    max_game = Game.objects.all().order_by('game_number').first()
    game = Game(game_number=max_game.game_number+1)
    game.save()
    return HttpResponseRedirect('/game')





