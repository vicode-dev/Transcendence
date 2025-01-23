from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from app.models import Game, Tournament
from django.core import serializers
from django.http import Http404, HttpResponseBadRequest, HttpResponseNotAllowed
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from lobby.utils.token import get_jwt_data
from django.conf import settings
from tournament.gameManagement import startGames, death
import datetime 
import asyncio, requests
from django.shortcuts import redirect
import random
import math

def render_redirect(request):
    jwtData = get_jwt_data(request)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and "error" not in jwtData:
        try:
            requests.post(f"http://user-management:8000/api/player/{jwtData['id']}/lastConnection/", cookies={"secret": settings.SECRET_KEY})
        except:
            pass
        return None
    url = request.path
    query_params = request.GET.copy()
    query_params["redirect_url"] = url[1:]
    if "error" in jwtData:
        new_url = f"/login/?{query_params.urlencode()}"
    else:
        new_url = f"/?{query_params.urlencode()}"
    return redirect(new_url)

def index(request):
    redirectObject = render_redirect(request)
    if redirectObject:
        return redirectObject
    return render(request, 'tournament/index.html')

@require_http_methods(["GET"])
def room(request, room_name):
    redirectObject = render_redirect(request)
    if redirectObject:
        return redirectObject
    if (not Tournament.objects.filter(pk=room_name).exists()):
        raise Http404("Tournament does not exist")
    if Tournament.objects.filter(pk=room_name).values_list("state", flat=True).first():
        return redirect(f"/tournament/{room_name}/dashboard/")
    return render(request, "tournament/room.html", {"room_name": room_name, "playercount": 0})

@require_http_methods(["POST"])
def create(request):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse("Unautorized", status=401)
    NewTournament = Tournament(gamesId=[],playersId=[])
    NewTournament.save()
    return JsonResponse({"id": NewTournament.tournamentId})

def closestPowerTwo(length):
    return 2 ** (math.ceil(math.log(length, 2)))

@require_http_methods(["POST"])
def start(request, room_name):
    if "error" in get_jwt_data(request):
        return HttpResponse("Unautorized", status=401)
    channel_layer = get_channel_layer()
    tournament = Tournament.objects.get(pk=room_name)
    if len(tournament.playersId) < 3:
        return HttpResponseBadRequest()
    tournament.state = True
    tournament.save()
    random.shuffle(tournament.playersId)
    if (len(tournament.playersId) % 2 != 0):
        tournament.playersId.insert(0, 0)
    length = closestPowerTwo(len(tournament.playersId))
    diff = length - len(tournament.playersId)
    for i in range(diff):
        tournament.playersId.append(None)
    new_length = 2 * length - 1
    tournament.playersId = [None if i < new_length - length else tournament.playersId[i - (new_length - length)] for i in range(new_length)]
    tournament.gamesId = [0 for i in range(new_length - length)]
    tournament.gamesUUID = [None for i in range(new_length - length)]
    tournament.save()
    startGames(tournament)
    # async_to_sync(channel_layer.group_send)(
    #     f'tournament_{room_name}',
    #     {
    #         'type': 'redirect',
    #         "url": f"{room_name}/dashboard/"
    #     }
    # )
    # async_to_sync(channel_layer.group_send)(
    #     f'tournament_{room_name}',
    #     {
    #         'type': 'stats',
    #         "players": tournament.playersId
    #     }
    # )
    return HttpResponse('')

async def dashboard(request, room_name):
    redirectObject = render_redirect(request)
    if redirectObject:
        return redirectObject
    tournament = None
    try:
        tournament = await sync_to_async(Tournament.objects.get)(pk=room_name)
    except:
        return HttpResponse(status=404)
    if tournament.state == False:
        return redirect(f"/tournament/{room_name}/") 
    return render(request, "tournament/dashboard.html", {"room_name": room_name, "playercount": 0})

def game(request, room_name, gameId):
    redirectObject = render_redirect(request)
    if redirectObject:
        return redirectObject
    try:
        result = Game.objects.get(pk=gameId)
        return render(request, "tournament/game.html", {"game": result, "render": 0, "online": True})
    except:
        return redirect(f"tournament/{room_name}/dashboard/")