import requests
import statistics
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from app.models import Game
from lobby.utils.token import get_jwt_data
from django.middleware.csrf import get_token
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

def startTournament():
    return

@require_http_methods(["GET"])
def game(request, gameId):
    redirect = render_redirect(request)
    if redirect:
        return redirect
    if not Game.objects.filter(pk=gameId).exists():
        raise Http404("Game does not exist")
    renderType = True if request.GET.get('render', "false") == "true" else False
    result = Game.objects.get(pk=gameId)
    if result.state == False:
        raise Http404("")
    if result.gameType == False:
        return render(request, "pong/pong.html", {"game": result, "render": renderType, "online": True})
    else:
        return render(request, "connect4/connect4.html", {"online": True})

@require_http_methods(["GET"])
def localgame(request):
    redirect = render_redirect(request)
    if redirect:
        return redirect
    localgame_url = reverse('localgame')
    maxPlayers = int(request.GET.get('maxPlayers', 2))
    gameType = int(request.GET.get('gameType', 0))
    renderType = True if request.GET.get('render', "false") == "true" else False
    if gameType == 1:
        return render(request, "connect4/connect4.html", {"online": False})
    else:
       return render(request, "pong/pong.html", {"game" : {"maxPlayers": maxPlayers, "score": [5,5,5,5] if maxPlayers == 4 else [0,0]}, "render": renderType, "online": False})

@require_http_methods(["POST"])
def matchmaking(request):
    jwtData = get_jwt_data(request)
    maxPlayers = int(request.GET.get('maxPlayers', 2))
    gameType = int(request.GET.get('gameType', 0))
    gamesQueried = Game.objects.filter(gameType=gameType, maxPlayers=maxPlayers)
    if not gamesQueried.exists():
        NewGame = Game(players=[], admin=jwtData["id"], score=[], maxPlayers=maxPlayers, gameType=gameType)
        NewGame.save()
        return JsonResponse({"gameId": NewGame.gameId})
    bestMatch = gamesQueried[0]
    bestMatchDiff = 10000
    playerElo = requests.get(f"http://user-management:8000/api/player/{jwtData["id"]}/elo").json()
    if gameType == 0:
        playerElo = playerElo["eloPong"]
    else:
        playerElo = playerElo["eloConnect"]
    for game in gamesQueried:
        rankings = []
        for player in game.players:
            elo = requests.get(f"http://user-management:8000/api/player/{player}/elo").json()
            if game.gameType == False:
                rankings.append(elo["eloPong"])
            else:
                rankings.append(elo["eloConnect"])
        if len(rankings):
            diff = abs(playerElo - statistics.median(rankings))
        else:
            diff = 9999
        if diff < bestMatchDiff:
            bestMatchDiff = diff
            bestMatch = game
    return JsonResponse({"gameId": bestMatch.gameId})

def home(request):
    redirect = render_redirect(request)
    if redirect:
        return redirect
    return render(request, "partials/index.html")

def singlePage(request):
    return render(request, "index.html")

def matchmaking_page(request):
    csrf_token = get_token(request)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'partials/matchmaking.html', {'csrf_token': csrf_token})
    return render(request, "matchmaking.html", {'csrf_token': csrf_token})

def game_select(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "partials/game_select.html")
    return render(request, "game_select.html")
    # return render_redirect(request)

def theme(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "partials/settings.html")
    return render(request, "settings.html")
    # return render_redirect(request)