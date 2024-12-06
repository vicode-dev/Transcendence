from django.http import HttpResponse, FileResponse
from django.http import JsonResponse
from django.core import serializers
from django.http import Http404, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.db.models import F, Func, Value
from . import blockchain
from app.models import User
from app.utils.token import get_jwt_data
from app.eloUpdater import elo
import requests, json, os

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

@require_http_methods(["GET"])
def setupContract(request):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    blockchain.setup()
    return HttpResponse(status=204)

#temp #players, score, pong/connect, startime
@csrf_exempt
@require_http_methods(["POST"])
def add(request):
    game = json.loads(request.body.decode('utf-8'))
    elo(game)
    blockchain.addGame(game["players"], game["score"], game["gameType"], int(game["endTime"] - game["startTime"]), game["startTime"], game["endTime"])
    return HttpResponse(status=204)

@require_http_methods(["GET"])
def getGamesNumber(request):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    return JsonResponse({'GameNumber': blockchain.getGamesNumber()}, status=200)

@require_http_methods(["GET"])
def addPlayer(request):
    playerId = int(request.GET.get('playerId', 0))
    if playerId == 0:
        return HttpResponseBadRequest()
    username = request.GET.get('username', "Arthur Dent")
    newUser = User(playerId=playerId, username=username)
    newUser.save()
    return HttpResponse(status=204)

@require_http_methods(["GET"])
def getGameById(request, id):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    return JsonResponse(blockchain.getGameById(id).to_dict())

@require_http_methods(["GET"])
def getTournamentById(request, id):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    return JsonResponse(blockchain.getTournamentById(id).to_dict())

@require_http_methods(["GET"])
def getPlayerById(request, playerId):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    if not User.objects.filter(pk=playerId).exists():
        raise Http404("User not found")
    result = User.objects.get(pk=playerId)
    return JsonResponse(result.json())

@require_http_methods(["GET"])
def playerHTML(request, playerId):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    if not User.objects.filter(pk=playerId).exists():
        raise Http404("User not found")
    username = User.objects.filter(pk=playerId).values_list("username", flat=True).first()
    return render(request, "userComponent.html", {"user": {"username": username, "playerId": playerId}})

@require_http_methods(["GET"])
def getPlayerGame(request, playerId):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    gameObject = blockchain.getGamesByPlayer(playerId)
    return JsonResponse([t.to_dict() for t in gameObject], safe=False)

@require_http_methods(["GET"])
def playerRole(request, playerId):
    value = User.objects.filter(pk=playerId).values_list("role", flat=True).first()
    if value:
        return JsonResponse({"role": value})
    else:
        raise Http404("User not found")

@require_http_methods(["GET"])
def playerElo(request, playerId):
    eloPong, eloConnect = User.objects.filter(pk=playerId).values_list("eloPong", "eloConnect").first()
    if eloPong:
        return JsonResponse({"eloPong": eloPong, "eloConnect": eloConnect})
    else:
        raise Http404("User not found")

@csrf_exempt
@require_http_methods(["GET", "POST"])
def playerAvatar(request, playerId):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    if request.method == "GET":
        if os.path.exists(f"/static/{playerId}.jpg"):
            return FileResponse(open(f"/static/{playerId}.jpg", 'rb'))
        elif os.path.exists(f"/static/{playerId}.jpeg"):
            return FileResponse(open(f"/static/{playerId}.jpeg", 'rb'))
        elif os.path.exists(f"/static/{playerId}.png"):
            return FileResponse(open(f"/static/{playerId}.png", 'rb'))
        else:
            return FileResponse(open("app/static/default.jpg", 'rb'))
        if value:
            return JsonResponse({"avatar": value})
        else:
            raise Http404("User not found")
    else:
        if jwtData["id"] != playerId and jwtData["role"] == "D":
            return HttpResponse(jwtData["error"], status=401)
        if not "profile_picture" in request.FILES:
            return HttpResponseBadRequest("No file turned in")
        file = request.FILES["profile_picture"]
        if file.content_type != "image/jpeg" and file.content_type != "image/png":
            return HttpResponseBadRequest("Wrong content Type")
        if os.path.exists(f"/static/{playerId}.jpg"):
            os.remove(f"/static/{playerId}.jpg")
        if os.path.exists(f"/static/{playerId}.jpeg"):
            os.remove(f"/static/{playerId}.jpeg")
        if os.path.exists(f"/static/{playerId}.png"):
            os.remove(f"/static/{playerId}.png")
        newFile = open(f"/static/{playerId}.{file.name.split('.')[-1]}", "wb")
        for chunk in file.chunks():
            newFile.write(chunk)
        newFile.close()
        return HttpResponse(status=204)

@require_http_methods(["GET"])
def getPlayerUsername(request, playerId):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    value = User.objects.filter(pk=playerId).values_list("username", flat=True).first()
    if value:
        return JsonResponse({"username": value})
    else:
        raise Http404("User not found")

@require_http_methods(["GET"])
def getPlayerFriends(request, playerId):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    value = User.objects.filter(pk=playerId).values_list("friends", flat=True).first()
    if value:
        return JsonResponse({"friends": value})
    else:
        raise Http404("User not found")

@csrf_exempt
@require_http_methods(["POST"])
def addFriend(request):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    friendId = int(request.GET.get('playerId', -1))
    if not User.objects.filter(pk=friendId).exists():
        return HttpResponseBadRequest()
    User.objects.filter(pk=jwtData["id"]).update(friends=Func(F('friends'), Value(friendId), function='array_append'))
    return HttpResponse(status=204)

@csrf_exempt
@require_http_methods(["POST"])
def removeFriend(request):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    friendId = int(request.GET.get('playerId', -1))
    User.objects.filter(pk=jwtData["id"]).update(
            friends=Func(F('friends'), Value(friendId), function='array_remove')
        )
    return HttpResponse(status=204)

@require_http_methods(["GET"])
def profil(request, playerId):
    redirect = render_redirect(request)
    if redirect:
        return redirect
    if User.objects.filter(pk=playerId).exists():
        user = User.objects.get(pk=playerId)
    else:
        playerId = 0
        user = User.objects.get(pk=playerId)
    games = blockchain.getGamesByPlayer(playerId)
    for i in range(len(games)):
        games[i].combined = list(zip(games[i].playerIds, games[i].score))
    jwtData = get_jwt_data(request)
    return render(request, "profil.html", {"user": user, "games": games, "id": jwtData["id"]})

@require_http_methods(["GET"])
def authProfil(request):
    redirect = render_redirect(request)
    if redirect:
        return redirect
    jwtData = get_jwt_data(request)
    if User.objects.filter(pk=jwtData["id"]).exists():
        user = User.objects.get(pk=jwtData["id"])
    games = blockchain.getGamesByPlayer(jwtData["id"])
    for i in range(len(games)):
        games[i].combined = list(zip(games[i].playerIds, games[i].score))
    return render(request, "profil.html", {"user": user, "games": games, "id": jwtData["id"]})

@require_http_methods(["GET"])
def settings(request):
    redirect = render_redirect(request)
    if redirect:
        return redirect
    jwtData = get_jwt_data(request)
    return render(request, "settings/index.html", {"playerId": jwtData["id"]})
