from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from app.models import Game, ChatMessage
from django.conf import settings
from django.http import Http404, HttpResponseBadRequest, HttpResponseNotAllowed
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from lobby.utils.token import get_jwt_data
import datetime, requests
from django.shortcuts import redirect

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
    return render(request, 'lobby/index.html')

def getRoom(request, room_name, jwtData):
    redirectObject = render_redirect(request)
    if redirectObject:
        return redirectObject
    if (not Game.objects.filter(pk=room_name).exists()):
        raise Http404("Lobby does not exist")
    if Game.objects.filter(pk=room_name).values_list("state", flat=True).first():
        return redirect(f"/game/{room_name}/")
    game = Game.objects.get(pk=room_name)
    admin = False
    if jwtData["id"] == game.admin or jwtData["role"] == "A":
        admin = True
    return render(request, "lobby/room.html", {"game": game, "admin": admin})

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
        if private == "0":
            newGame.private = False
            newGame.save()
        elif private == "1":
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

@require_http_methods(["POST", "GET"])
@csrf_exempt
def room(request, room_name):
    jwtData = get_jwt_data(request)
    if request.method == "GET":
        return getRoom(request, room_name, jwtData)
    else:
        return postRoom(request, room_name, jwtData)

@require_http_methods(["POST"])
@csrf_exempt
def create(request):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse("Unautorized", status=401)
    # body = json.loads(request.body)
    gameType = int(request.GET.get('gameType', 0))
    maxPlayers = int(request.GET.get('maxPlayers', 2))
    if gameType == False:
        NewGame = Game(players=[], admin=jwtData["id"], score=[0 if maxPlayers == 2 else 5 for i in range(maxPlayers)], maxPlayers=maxPlayers, startTime=datetime.datetime.now(), gameType=False)
    else:
        NewGame = Game(players=[], admin=jwtData["id"], score=[], maxPlayers=2, startTime=datetime.datetime.now(), gameType=True)
    NewGame.save()
    return JsonResponse({"id": NewGame.gameId})

@require_http_methods(["POST"])
@csrf_exempt
def start(request, room_name):
    if "error" in get_jwt_data(request):
        return HttpResponse("Unautorized", status=401)
    jwtData = get_jwt_data(request)
    channel_layer = get_channel_layer()
    game = Game.objects.get(pk=room_name)
    if len(game.players) != game.maxPlayers:
        return HttpResponseBadRequest()
    if jwtData["id"] != game.admin and jwtData["role"] != "A":
        return HttpResponse("Unautorized", status=401)
    game.state = True
    game.save()
    messages = ChatMessage.objects.filter(chatId=room_name)
    for message in messages:
        message.delete()
    async_to_sync(channel_layer.group_send)(
        f'lobby_{room_name}',
        {
            'type': 'lobby_redirect',
        }
    )
    return HttpResponse('')
