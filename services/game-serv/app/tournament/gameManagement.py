from app.models import Tournament, Game, ChatMessage
from django.utils.timezone import now
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
import math
import logging, requests

logger = logging.getLogger('app')
def startGames(tournament):
    channel_layer = get_channel_layer()
    for i in range(len(tournament.playersId) - 1, 0, -2):
        if(tournament.playersId[i]):
            if (tournament.playersId[i - 1]):
                game = Game(players=[tournament.playersId[i], tournament.playersId[i - 1]], admin=0, score=[0,0], maxPlayers=2, startTime=now(), gameType=False, state=True)
                game.save()
                tournament.gamesUUID[math.floor((i - 1) / 2)] = game.pk
                tournament.save()
                async_to_sync(channel_layer.group_send)(
                    f'tournament_{tournament.pk}',
                    {
                        'type': 'redirectOne',
                        'id': tournament.playersId[i],
                        "url": f"{tournament.pk}/game/{game.pk}/"
                    })
                async_to_sync(channel_layer.group_send)(
                    f'tournament_{tournament.pk}',
                    {
                        'type': 'redirectOne',
                        'id': tournament.playersId[i - 1],
                        "url": f"{tournament.pk}/game/{game.pk}/"
                    })
            else:
                logger.debug("Redirect from startGames")
                async_to_sync(channel_layer.group_send)(
                    f'tournament_{tournament.pk}',
                    {
                        'type': 'redirectOne',
                        'id': tournament.playersId[i],
                        "url": f"{tournament.pk}/dashboard/"
                    })
        else:
            continue

async def war(tournament):
    channel_layer = get_channel_layer()
    for i in range(len(tournament.gamesUUID)):
        if tournament.gamesUUID[i] == None:
            leftChild = tournament.playersId[2 * i + 1]
            rightChild = tournament.playersId[2 * i + 2]
            if (leftChild and rightChild and leftChild != 0 and rightChild != 0):
                if leftChild in tournament.disconnectedPlayersId:
                    logger.debug("LEFT CHILD")
                    logger.debug(tournament.playersId)
                    logger.debug(tournament.disconnectedPlayersId)
                    tournament.playersId[2 * i + 1] = 0
                    await death(tournament)
                    return
                elif rightChild in tournament.disconnectedPlayersId:
                    logger.debug("RIGHT CHILD")
                    logger.debug(tournament.playersId)
                    logger.debug(tournament.disconnectedPlayersId)
                    tournament.playersId[2 * i + 2] = 0
                    await death(tournament)
                    return
                game = await sync_to_async(Game)(players=[leftChild, rightChild], admin=0, score=[0,0], maxPlayers=2, startTime=now(), gameType=False, state=True)
                await sync_to_async(game.save)()
                tournament.gamesUUID[i] = game.pk
                await sync_to_async(tournament.save)()
                await channel_layer.group_send(
                    f'tournament_{tournament.pk}',
                    {
                        'type': 'redirectOne',
                        'id': leftChild,
                        "url": f"{tournament.pk}/game/{game.pk}/"
                    })
                await channel_layer.group_send(
                    f'tournament_{tournament.pk}',
                    {
                        'type': 'redirectOne',
                        'id': rightChild,
                        "url": f"{tournament.pk}/game/{game.pk}/"
                    })

async def death(tournament):
    channel_layer = get_channel_layer()
    logger.debug(tournament.playersId)
    for i in range(len(tournament.gamesUUID)):
        if (tournament.gamesUUID[i] != None):
            game = await sync_to_async(Game.objects.get)(pk=tournament.gamesUUID[i])
            if (game.GameIdEth):
                tournament.gamesId[i] = game.GameIdEth
                if game.score[0] == 10:
                    tournament.playersId[i] = game.players[0]
                elif game.score[1] == 10:
                    tournament.playersId[i] = game.players[1]
                elif game.score[0] == 0 and game.score[1] == 1:
                    tournament.playersId[i] = game.players[1]
                elif game.score[0] == 1 and game.score[1] == 0:
                    tournament.playersId[i] = game.players[0]
                elif game.score[0] == 0 and game.score[1] == 0:
                    tournament.playersId[i] = 0
        else:
            leaves = (len(tournament.playersId) + 1) / 2
            leftChild = tournament.playersId[2 * i + 1]
            rightChild = tournament.playersId[2 * i + 2]
            if (rightChild == 0 and leftChild == 0) or (leftChild == None and rightChild == None and (2 * i + 1) >= len(tournament.playersId) - leaves):
                tournament.playersId[i] = 0 
            elif (leftChild == 0):
                tournament.playersId[i] = rightChild
            elif (rightChild == 0):
                tournament.playersId[i] = leftChild
        await sync_to_async(tournament.save)()
    if tournament.playersId[0] != None:
        logger.debug("Winner")
        reponse = requests.post("http://user-management:8000/api/tournament/add", json=tournament.toJson()).json()
        # asyncio.sleep(5000)
        messages = await sync_to_async(ChatMessage.objects.filter)(chatId=tournament.tournamentId)
        await sync_to_async(messages.delete)()
        for game in tournament.gamesUUID:
            if game:
                gameObject = await sync_to_async(Game.objects.get)(pk=game)
                await sync_to_async(gameObject.delete)()
        logger.debug("Tournament redirected")
        await channel_layer.group_send(
                    f'tournament_{tournament.pk}',
                    {
                        'type': 'redirect',
                        "url": f"summary/{reponse["tournamentId"]}/"
                    })
        logger.debug("Tournament deleted")
        await sync_to_async(tournament.delete)()
        return
    await war(tournament)
