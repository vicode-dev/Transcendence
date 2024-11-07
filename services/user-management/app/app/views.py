from django.http import HttpResponse, FileResponse
from django.http import JsonResponse
from django.core import serializers
from django.http import Http404
from django.shortcuts import render
from . import blockchain
from app.models import User
import requests, json, os

def index(request):
    html = "<html><body>%s</body></html>" % blockchain.test()
    return HttpResponse(html)

def setupContract(request):
    blockchain.setup()
    return HttpResponse("<h1>Ok</h1>")

def getGamesNumber(request):
    return JsonResponse({'GameNumber': blockchain.getGamesNumber()}, status=200)

def add(request):
    blockchain.addGame([1, 2], [2, 3], False, 24, 0, 23)
    return HttpResponse("<h1>Ok</h1>")

def getGameById(request, id):
    return JsonResponse(blockchain.getGameById(id).to_dict())

def getTournamentById(request, id):
    return JsonResponse(blockchain.getTournamentById(id).to_dict())


def getPlayerById(request, playerId):
    # try:
        result = User.objects.get(pk=playerId)
        return JsonResponse(result.json())
    # except:
    #     raise Http404("User not found")

def getPlayerGame(request, playerId):
    gameObject = blockchain.getGamesByPlayer(playerId)
    return JsonResponse([t.to_dict() for t in gameObject], safe=False)

def playerAvatar(request, playerId):
    if request.method == "GET":
        if os.path.exists(f"/static/{playerId}.jpg"):
            return FileResponse(open(f"/static/{playerId}.jpg", 'rb'))
        elif os.path.exists(f"/static/{playerId}.jpeg"):
            return FileResponse(open(f"/static/{playerId}.jpeg", 'rb'))
        else:
            return FileResponse(open("app/static/default.jpg", 'rb'))
        # value = User.objects.filter(pk=playerId).values_list("profilePicture", flat=True).first()
        if value:
            return JsonResponse({"avatar": value})
        else:
            raise Http404("User not found")
    elif request.method == "POST":
        return

def getPlayerUsername(request, playerId):
    value = User.objects.filter(pk=playerId).values_list("username", flat=True).first()
    if value:
        return JsonResponse({"username": value})
    else:
        raise Http404("User not found")

def getPlayerFriends(request, playerId):
    value = User.objects.filter(pk=playerId).values_list("friends", flat=True).first()
    if value:
        return JsonResponse({"friends": value})
    else:
        raise Http404("User not found")

def addplayer(request):
    test = User(1, "Rachel", 130, [3], "Member")
    test.save()
    return HttpResponse("<h1>Ok</h1>")

def profile(request, playerId):
    if User.objects.filter(pk=playerId).exists():
        result = User.objects.get(pk=playerId)
    else:
        playerId = 0
        result = User.objects.get(pk=playerId)
    games = blockchain.getGamesByPlayer(playerId)
    for j in range(len(games)):
        for i in range(len(games[j].playerIds)):
            games[j].playerIds[i] = {
                "username": User.objects.filter(pk=games[j].playerIds[i]).values_list("username", flat=True).first(), 
                "url": f"/profile/{games[j].playerIds[i]}", 
                "score": games[j].score[i]
                }
            if not games[j].playerIds[i]:
                games[j].playerIds[i].username = "unkown"
    friends= [None] * len(result.friends)
    for i in range(len(result.friends)):
        friends[i] = {
            "username": User.objects.filter(pk=result.friends[i]).values_list("username", flat=True).first(), 
            "url": f"/profile/{result.friends[i]}"
            }
    return render(request, "profile.html", {"user": result, "games": games, "friends": friends})

def settings(request):
    return render(request, "settings/index.html", {"playerId": 0})

#Temp function
def login(request):
    return render(request, "login-temp.html")
def auth(request):
        return request.COOKIES["id"]