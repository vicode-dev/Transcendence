from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from app.models import Game, Tournament
from django.core import serializers
from django.http import Http404, HttpResponseBadRequest, HttpResponseNotAllowed
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from lobby.utils.token import get_jwt_data
import datetime 
import asyncio
from django.shortcuts import redirect

def render_redirect(request):
    jwtData = get_jwt_data(request)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and "error" not in jwtData:
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

def getRoom(request, room_name, jwtData):
    redirectObject = render_redirect(request)
    if redirectObject:
        return redirectObject
    if (not Tournament.objects.filter(pk=room_name).exists()):
        raise Http404("Tournament does not exist")
    if Tournament.objects.filter(pk=room_name).values_list("state", flat=True).first():
        return redirect(f"/tournament/{room_name}/dashboard/")
    # game = Tournament.objects.get(pk=room_name)
    # admin = False
    # if jwtData["id"] == game.admin or jwtData["role"] == "A":
    #     admin = True
    return render(request, "tournament/room.html", {"room_name": room_name, "playercount": 0})

def postRoom(request, room_name, jwtData):
    if (not Game.objects.filter(pk=room_name, state=False).exists()):
        raise Http404("Lobby does not exist")
    newGame = Game.objects.get(pk=room_name)
    if jwtData["id"] == newGame.admin or jwtData["role"] == "A":
        maxPlayers = request.GET.get('maxPlayers', 0)
        if maxPlayers == '2' or maxPlayers == '4':
            newGame.maxPlayers = maxPlayers
            newGame.save()
        private = request.GET.get('private', 3)
        if private == 0:
            newGame.private = False
            newGame.save()
        elif private == 1:
            newGame.private = True
            newGame.save()
        async_to_sync(get_channel_layer().group_send)(f"lobby_{str(room_name)}",
            {
                'type': 'lobby_game',
                'players': newGame.players, 
                'maxPlayers': newGame.maxPlayers
            })
        return HttpResponse(status=204)
    return HttpResponseNotAllowed()

@csrf_exempt
@require_http_methods(["POST", "GET"])
def room(request, room_name):
    jwtData = get_jwt_data(request)
    if request.method == "GET":
        return getRoom(request, room_name, jwtData)
    else:
        return postRoom(request, room_name, jwtData)

@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse("Unautorized", status=401)
    NewTournament = Tournament(gamesId=[],playersId=[])
    NewTournament.save()
    return JsonResponse({"id": NewTournament.tournamentId})

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
    async_to_sync(channel_layer.group_send)(
        f'tournament_{room_name}',
        {
            'type': 'redirect',
            "url": f"{room_name}/dashboard/"
        }
    )
    return HttpResponse('')

def dashboard(request, room_name):
    redirectObject = render_redirect(request)
    if redirectObject:
        return redirectObject
    return render(request, "tournament/dashboard.html", {"room_name": room_name, "playercount": 0})

