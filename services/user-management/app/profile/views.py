from django.http import HttpResponse, FileResponse
from django.http import JsonResponse
from django.http import Http404, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.db.models import F, Func, Value
from . import blockchain
from django.conf import settings as GlobalSettings
from profile.models import User
from profile.utils.token import get_jwt_data
from profile.eloUpdater import elo
import requests, json, os, datetime
import logging
from django.utils.translation import gettext as _
from datetime import timedelta
from django.utils.timezone import now


logger = logging.getLogger('profile')
def render_redirect(request):
    jwtData = get_jwt_data(request)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and "error" not in jwtData:
        if User.objects.filter(pk=jwtData["id"]).exists():
            User.objects.filter(pk=jwtData["id"]).update(lastConnection=now())
        return None
    url = request.path
    query_params = request.GET.copy()
    query_params["redirect_url"] = url[1:]
    if "error" in jwtData:
        new_url = f"/login/?{query_params.urlencode()}"
    else:
        new_url = f"/?{query_params.urlencode()}"
    return redirect(new_url)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def playerLastConnection(request, playerId):
    jwtData = get_jwt_data(request)
    if "error" in jwtData and request.COOKIES.get("secret") != GlobalSettings.SECRET_KEY:
        return HttpResponse(jwtData["error"], status=401)
    if request.method == "POST":
        if request.COOKIES.get("secret") != GlobalSettings.SECRET_KEY:
            if jwtData["id"] != playerId and jwtData["role"] == "D":
                return HttpResponse(status=401)
        if not User.objects.filter(pk=playerId).exists():
            raise Http404("User not found")
        User.objects.filter(pk=playerId).update(lastConnection=now())
        return HttpResponse(status=204)
    if request.method == "GET":
        value = User.objects.filter(pk=playerId).values_list("lastConnection", flat=True).first()
        if value:
            return JsonResponse({"lastConnection": value})
        else:
            raise Http404("User not found")

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
    tx_receipt = blockchain.addGame(game["players"], game["score"], game["gameType"], game["startTime"], game["endTime"])
    return JsonResponse({"gameId": tx_receipt})

@csrf_exempt
@require_http_methods(["POST"])
def addTournament(request):
    tournament = json.loads(request.body.decode('utf-8'))
    for i in range(len(tournament["playersId"])):
        if tournament["playersId"][i] == None:
            tournament["playersId"][i] = 0
    tx_receipt = blockchain.addTournament(tournament["gamesId"], tournament["playersId"])
    return JsonResponse({"tournamentId": tx_receipt})

@require_http_methods(["GET"])
def getGamesNumber(request):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    return JsonResponse({'GameNumber': blockchain.getGamesNumber()}, status=200)

@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def Player(request):
    playerId = int(request.GET.get('playerId', 0))
    if playerId == 0:
        return HttpResponseBadRequest()
    if request.method == "GET":
        username = request.GET.get('username', "Arthur Dent")
        newUser = User(playerId=playerId, username=username, role=('D' if playerId != 1 else 'A'))
        newUser.save()
        return HttpResponse(status=204)
    elif request.method == "DELETE":
        if User.objects.filter(pk=playerId).exists():
            User.objects.filter(pk=playerId).delete()
            if os.path.exists(f"/static/{playerId}.jpg"):
                os.remove(f"/static/{playerId}.jpg")
            elif os.path.exists(f"/static/{playerId}.jpeg"):
                os.remove(f"/static/{playerId}.jpeg")
            elif os.path.exists(f"/static/{playerId}.png"):
                os.remove(f"/static/{playerId}.png")
            return HttpResponse(status=204)
        else:
            raise Http404("User not found")

@require_http_methods(["GET"])
def getGameById(request, id):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    try:
        game = blockchain.getGameById(id).to_dict()
        return JsonResponse(game)
    except Exception as e:
        raise Http404("Game not found")

@require_http_methods(["GET"])
def getTournamentById(request, id):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    try:
        games = blockchain.getTournamentById(id)
        return JsonResponse(games.to_dict())
    except:
        raise Http404("Tournament not found")

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
    user = User.objects.get(pk=playerId)
    user.lastConnection = True if (now() - user.lastConnection) <= timedelta(minutes=5) else False
    return render(request, "userComponent.html", {"user": user})

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

@require_http_methods(["GET", "POST"])
def playerTheme(request, playerId):
    jwtData = get_jwt_data(request)
    if request.method == "POST":
        if "error" in jwtData:
            return HttpResponse(jwtData["error"], status=401)
        theme = json.loads(request.body.decode('utf-8'))["theme"]
        if len(theme) != 3:
            return HttpResponseBadRequest()
        theme = [int(theme[0], 16), int(theme[1], 16), int(theme[2], 16)]
        if User.objects.filter(pk=playerId).exists():
            User.objects.filter(pk=playerId).update(theme=theme)
            return HttpResponse(status=204)
        else:
            raise Http404("User not found")
    elif request.method == "GET":
        value = User.objects.filter(pk=playerId).values_list("theme", flat=True).first()
        if value:
            # value = [hex(value[0]), hex(value[1]), hex(value[2])]
            # for i in range(len(value)):
            #     if value[i] == "0x0":
            #         value[i] = "0x000000"
            # return JsonResponse({"theme": value})
            value = [hex(v)[2:].zfill(6) for v in value]
            value = [f"0x{v}" for v in value]
            return JsonResponse({"theme": value})
        else:
            raise Http404("User not found")

@require_http_methods(["GET"])
def playerElo(request, playerId):
    eloPong, eloConnect = User.objects.filter(pk=playerId).values_list("eloPong", "eloConnect").first()
    if eloPong:
        return JsonResponse({"eloPong": eloPong, "eloConnect": eloConnect})
    else:
        raise Http404("User not found")

@require_http_methods(["POST"])
def playersElo(request):
    playerIds = json.loads(request.body.decode('utf-8'))["playerIds"]
    for i in range(len(playerIds)):
        playerIds[i] = int(playerIds[i])
    elos = User.objects.filter(pk__in=playerIds).values("eloPong", "eloConnect")
    return JsonResponse(list(elos))

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
            return FileResponse(open("profile/static/default.jpg", 'rb'))
    else:
        if jwtData["id"] != playerId and jwtData["role"] == "D":
            return HttpResponse(jwtData["error"], status=401)
        if not "avatar" in request.FILES:
            return HttpResponseBadRequest("No file turned in")
        file = request.FILES["avatar"]
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

@require_http_methods(["GET", "POST"])
def PlayerUsername(request, playerId):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    if request.method == "GET":
        value = User.objects.filter(pk=playerId).values_list("username", flat=True).first()
        if value:
            return JsonResponse({"username": value})
        else:
            raise Http404("User not found")
    else:
        if jwtData["id"] != playerId and jwtData["role"] == "D":
            return HttpResponse(status=401)
        request_body = json.loads(request.body.decode('utf-8'))
        if "username" in request_body:
            username = request_body["username"]
            username = username.strip()
            if len(username) < 4 or len(username) > 19:
                return HttpResponseBadRequest("Username size must be between 8 and 19 characters.")
            User.objects.filter(pk=playerId).update(username=username)
            return HttpResponse(status=204)
        else:
            return HttpResponseBadRequest("No username turned in")

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
@require_http_methods(["GET"])
def rgpdPlayers(request):
    players = User.objects.filter(lastConnection=now() - timedelta(days=1095)).values_list("playerId", flat=True)
    return JsonResponse({"ids": list(players)})

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
    jwtData = get_jwt_data(request)
    tournaments = blockchain.getTournamentByPlayer(playerId)
    for i in range(len(tournaments)):
        tournaments[i].date = datetime.datetime.fromtimestamp(blockchain.getGameById(tournaments[i].gameIds[0]).endTime)
    for i in range(len(games)):
        games[i].combined = list(zip(games[i].playerIds, games[i].score))
    return render(
        		request, "profil.html",
          	{
              "user": user, "games": games, "tournaments": tournaments,
              "id": jwtData["id"]
           	}
        )

@require_http_methods(["GET"])
def authProfil(request):
    redirect = render_redirect(request)
    if redirect:
        return redirect
    jwtData = get_jwt_data(request)
    if User.objects.filter(pk=jwtData["id"]).exists():
        user = User.objects.get(pk=jwtData["id"])
    else:
        user = User.objects.get(pk=0)
    games = blockchain.getGamesByPlayer(jwtData["id"])
    tournaments = blockchain.getTournamentByPlayer(jwtData["id"])
    for i in range(len(tournaments)):
        last = tournaments[i].gameIds[0]
        j = 1
        while last == 0:
            last = tournaments[i].gameIds[j]
            j += 1
        tournaments[i].date = datetime.datetime.fromtimestamp(blockchain.getGameById(last).endTime)
    for i in range(len(games)):
        games[i].combined = list(zip(games[i].playerIds, games[i].score))
    return render(request, "profil.html", {"user": user, "games": games, "tournaments": tournaments, "id": jwtData["id"]})

@require_http_methods(["GET"])
def settings(request):
    redirect = render_redirect(request)
    if redirect:
        return redirect
    jwtData = get_jwt_data(request)
    if not User.objects.filter(pk=jwtData["id"]).exists():
        raise Http404("User not found")
    user = User.objects.get(pk=jwtData["id"])
    try:
        otp_enabled = requests.get(
            headers={
                "Authorization": os.environ.get("JWT_SECRET_KEY")
            },
            url="http://authentication:8000/api/otp/enabled/",
            cookies={
                "session":
                    request.COOKIES.get("session")
            }).text
    except requests.RequestException as e:
        otp_enabled = "False"

    return render(
        request, "settings/index.html",
        {
            "playerId": jwtData["id"], "user": user,
            "available_languages": dict(GlobalSettings.LANGUAGES).keys(),
            "otp_enabled": otp_enabled
        }
    )

@require_http_methods(["GET"])
def tournament(request, tournamentId):
    redirect = render_redirect(request)
    if redirect:
        return redirect
    games = []
    try:
        tournament = blockchain.getTournamentById(tournamentId)["gamesId"]
    except:
        raise Http404("Tournament not found")
    for i in tournament:
        games.append(blockchain.getGameById(i))
    for i in range(len(games)):
        games[i].combined = list(zip(games[i].playerIds, games[i].score))
    return render(request, "tournament.html", {"tournament": blockchain.getTournamentById(tournamentId), "games": games})

@require_http_methods(["GET"])
def getAllTournaments(request):
    jwtData = get_jwt_data(request)
    if "error" in jwtData:
        return HttpResponse(jwtData["error"], status=401)
    tournaments = blockchain.getAllTournaments()
    return JsonResponse([t.to_dict() for t in tournaments], safe=False)