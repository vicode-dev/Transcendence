from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from app.models import Game
from django.core import serializers
from django.http import Http404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json, datetime
# Create your views here.


def index(request):
    return render(request, "lobby/index.html")


def room(request, room_name):
    try:
        result = Game.objects.get(pk=room_name)
        return render(request, "lobby/room.html", {"room_name": room_name, "playercount": 0, "maxplayer": result.max_player})
    except:
        raise Http404("Lobby does not exist")

@require_http_methods(["POST"])
def create(request):
    body = json.loads(request.body)
    # body.gameId
    NewGame = Game(max_player=body['maxplayer'], start_time=datetime.datetime.now())
    NewGame.save()
    serialized_obj = serializers.serialize('json', [ NewGame, ])
    return JsonResponse(serialized_obj, safe=False)

def start(request):
    body = json.loads(request.body)
    channel_layer = get_channel_layer()
    game = Game.objects.get(pk=body['room_name'])
    game.state = True
    game.start_time = datetime.datetime.now()
    game.save()
    async_to_sync(channel_layer.group_send)(
        f'lobby_{body['room_name']}',
        {
            'type': 'lobby_redirect',
        }
    )
    return HttpResponse('')