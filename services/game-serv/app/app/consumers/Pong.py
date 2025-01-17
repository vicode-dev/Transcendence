import json, time, math
import asyncio
from app.models import Game
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.utils.timezone import now
from asgiref.sync import sync_to_async
import requests
import logging

logger = logging.getLogger('app')
GGDD = {} # Global Game Data Dictionary
SIZE = 9
PADDLE_SIZE = 1.5
PADDLE_WIDTH = 0.25
BALL_SIZE = 0.125
TICK_RATE = 1 / 20
MAX_SPEED = 10
INIT_SPEED = 2

class PongConsumer(AsyncWebsocketConsumer):

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        if self.scope["token_check"]["id"] in GGDD[self.room_name].playersId:
            GGDD[self.room_name].playersId.remove(self.scope["token_check"]["id"])
            if GGDD[self.room_name].started == True:
                await self.channel_layer.group_send(self.room_group_name, {'type': 'freeze', "state": True})

    async def close_connection(self, event):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        await self.close()

    async def freeze(self, event):
        GGDD[self.room_name].freeze = event["state"]
        players= []
        for player in GGDD[self.room_name].playersOrder:
            if player not in GGDD[self.room_name].playersId:
                players.append(player)
        GGDD[self.room_name].freeze = event["state"]
        await self.send(text_data=json.dumps({
            'type':'freeze',
            'state': event["state"],
            'players': players,
        }))

    async def tick_data(self, event):
        await self.send(text_data=json.dumps({
            'type':'tick_data',
            'P':event["P"],
            'Ball': event["Ball"]
        }))

    async def score_update(self, event):
        await self.send(text_data=json.dumps({
            'type':'score_update',                                                                                                                                                                                                                                
            'scores': event["score"],
        }))

    async def init(self, event):
        await self.send(text_data=json.dumps({
            'type':'init',
            'playersList':event["playersList"]
        }))

    async def get_index(self):
        for i in range(len(GGDD[self.room_name].playersOrder)):
            if GGDD[self.room_name].playersOrder[i] == self.scope["token_check"]["id"]:
                return i

    async def game_end(self, event):
        winner = 0 
        if len(GGDD[self.room_name].playersOrder) == 2:
            if GGDD[self.room_name].score[1] == 10:
                winner = 1
        else:
            for i in range(len(GGDD[self.room_name].score)):
                if GGDD[self.room_name].score[i] == 1:
                    winner = i
                    break
        logger.debug("GAME END")
        logger.debug(GGDD[self.room_name].score)
        logger.debug(self.index)
        await self.send(text_data=json.dumps({
            'type':'game_end',
            'score':GGDD[self.room_name].score[self.index],
            'winner':GGDD[self.room_name].playersOrder[winner]
        }))

class Ball:

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._angle = 180
        self._speed = INIT_SPEED

    def toJson(self):
        return {
            "x": self._x,
            "y": self._y,
            "angle": self._angle,
            "speed": self._speed
        }

class Player:

    def __init__(self, x, y):
        self._y = y
        self._x = x

    def toJson(self):
        return {
            "x": self._x,
            "y": self._y
        }

class GameData:

    def __init__(self, playersOrder, nb_players):
        if (nb_players == 2):
            self.score = [0, 0]
            self.paddles = [Player(0, 3.75), Player(8.75, 3.75)]
            self.playersMove = [0, 0]
        else:
            self.score = [5, 5, 5, 5]
            self.paddles = [Player(0, 3.75), Player(8.75, 3.75),  Player(3.75, 0), Player(3.75, 8.75)]
            self.playersMove = [0, 0, 0, 0]
        self.ball = Ball(4.5, 4.5)
        self.playersOrder = playersOrder
        self.playersId = []
        self.started = False
        self.freeze = False


async def initGameData(room_name, nb_players):
    if room_name not in GGDD:
        players = await getPlayersIdsInGame(room_name)
        GGDD[room_name] = GameData(players, nb_players)
    return

@database_sync_to_async
def getPlayersIdsInGame(room_name):
    # logger.debug(Game.objects.filter(pk=room_name).values('players').first())
    return Game.objects.filter(pk=room_name).values('players').first()["players"]

@database_sync_to_async
def game_exists(room_name, nb_players):
    return Game.objects.filter(pk=room_name, gameType=False, maxPlayers=nb_players, endTime=None).exists()

@database_sync_to_async
def isPlayerIdInGame(gameId, playerId):
    return Game.objects.filter(pk=gameId, players__contains=[playerId]).exists() 

@database_sync_to_async
def getGameById(gameId):
	return Game.objects.get(pk=gameId)

@database_sync_to_async
def updateModelScore(room_name, score):
    nb =  Game.objects.filter(pk=room_name).update(score=score)
    return nb


async def sleep(elapsedTime, room_name):
    await asyncio.sleep(max(0, TICK_RATE - elapsedTime))
    timeout = int(time.time())
    entered = False
    while GGDD[room_name].freeze == True:
        await asyncio.sleep(TICK_RATE)
        if int(time.time()) - timeout == 60:
            for i in range(len(GGDD[room_name].playersOrder)):
                GGDD[room_name].score[i] = 1 if GGDD[room_name].playersOrder[i] in GGDD[room_name].playersId else 0
            entered = False
            break
        entered = True
    if entered == True:
        await asyncio.sleep(3)


def willHitLeftPaddle(ball, px, py, x, y):
    if ((x - BALL_SIZE < px + PADDLE_WIDTH and py <= y - BALL_SIZE and y - BALL_SIZE <= py + PADDLE_SIZE)):
        ball._x = px + PADDLE_WIDTH + BALL_SIZE
    elif (x - BALL_SIZE < px + PADDLE_WIDTH and py <= y + BALL_SIZE and y + BALL_SIZE <= py + PADDLE_SIZE):
        ball._x = px + PADDLE_WIDTH + BALL_SIZE
    else:
        return False
    return True

def willHitRightPaddle(ball, px, py, x, y):
    if ((px < x + BALL_SIZE and py <= y + BALL_SIZE and y + BALL_SIZE <= py + PADDLE_SIZE)):
        ball._x = px - PADDLE_WIDTH - BALL_SIZE
    elif ((px < x + BALL_SIZE and py <= y - BALL_SIZE and y - BALL_SIZE <= py + PADDLE_SIZE)):
        ball._x = px - PADDLE_WIDTH - BALL_SIZE
    else:
        return False
    return True

def willHitTopPaddle(ball, px, py, x, y):
    if ((y - BALL_SIZE < py + PADDLE_WIDTH and px <= x - BALL_SIZE and x - BALL_SIZE <= px + PADDLE_SIZE)):
        ball.y = py + PADDLE_WIDTH + BALL_SIZE
    elif ((y - BALL_SIZE < py + PADDLE_WIDTH and px <= x + BALL_SIZE and x + BALL_SIZE <= px + PADDLE_SIZE)):
        ball.y = py + PADDLE_WIDTH + BALL_SIZE
    else:
        return False
    return True

def willHitBottomPaddle(ball, px, py, x, y):
    if ((py < y + BALL_SIZE and px <= x + BALL_SIZE and x + BALL_SIZE <= px + PADDLE_SIZE)):
        ball.y = py - BALL_SIZE
    elif (py < y + BALL_SIZE and px <= x - BALL_SIZE and x - BALL_SIZE <= px + PADDLE_SIZE):
        ball.y = py - BALL_SIZE
    else:
        return False
    return True

def hitWall(x):
    if x - BALL_SIZE <= 0 or x + BALL_SIZE >= SIZE:
        return True
    return False

def willHitWall(x):
    if (x - BALL_SIZE < 0 or x + BALL_SIZE > SIZE):
        return True
    return False

def ballHitPlayer(ball, startAngle, diff, ballPos):
    ball._angle = (360 + startAngle + (diff / (PADDLE_SIZE + 2 * BALL_SIZE)) * (ballPos + BALL_SIZE)) % 360

def paddleMove(room_name):
    length = len(GGDD[room_name].playersMove)
    for i in range(length):
        match GGDD[room_name].playersMove[i]:
            case 1:
                if (length == 2 and GGDD[room_name].paddles[i]._y < SIZE - PADDLE_SIZE):
                    GGDD[room_name].paddles[i]._y += 0.25
                elif (i < 2 and GGDD[room_name].paddles[i]._y < SIZE - PADDLE_SIZE - PADDLE_WIDTH):
                    GGDD[room_name].paddles[i]._y += 0.25
                elif i >= 2 and GGDD[room_name].paddles[i]._x < SIZE - PADDLE_SIZE - PADDLE_WIDTH:
                    GGDD[room_name].paddles[i]._x += 0.25
            case -1:
                if length == 2 and GGDD[room_name].paddles[i]._y > 0:
                    GGDD[room_name].paddles[i]._y -= 0.25
                elif i < 2 and GGDD[room_name].paddles[i]._y > PADDLE_WIDTH:
                    GGDD[room_name].paddles[i]._y -= 0.25
                elif i >= 2 and GGDD[room_name].paddles[i]._x > PADDLE_WIDTH:
                    GGDD[room_name].paddles[i]._x -= 0.25
        GGDD[room_name].playersMove[i] = 0

def newPoint(score, idx):
    score[idx] -= 1
    for i in range(4):
        if i != idx and score[i] <= 0 and score[idx] == 0:
            score[i] -= 1

def victory(room_name, nb_players):
    score = GGDD[room_name].score
    if nb_players == 2:
        if score[0] == 10 or score[1] == 10:
            return True
    else:
        count = 0
        win = 0
        for i in range(4):    
            if (score[i] <= 0):
                count += 1
            else:
                win = i
            if (count == 3):
                score[win] = 1
                newPoint(score, win)
                GGDD[room_name].score = [(i * -1) + 1 for i in score]
                # logger.debug(score)
                return True
    return False


async def gameLoop(room_name, nb_players, ballMovement):
    GGDD[room_name].started = True
    await get_channel_layer().group_send(f'game_{room_name}',{'type': 'freeze','state': False}
    )
    await asyncio.sleep(3)
    game = await getGameById(room_name)
    game.startTime = now()
    sync_to_async(game.save)()
    await get_channel_layer().group_send(f'game_{room_name}',{'type': 'init','playersList': GGDD[room_name].playersOrder}
    )
    while not GGDD[room_name].freeze:
        startTime = time.time()
        if victory(room_name, nb_players) == True:
            # await get_channel_layer().group_send(f'game_{room_name}', {'type': 'freeze','state': True})
            await get_channel_layer().group_send(f'game_{room_name}', {'type': 'game_end'})
            break
        paddleMove(room_name)
        await ballMovement(GGDD[room_name].score, GGDD[room_name].ball, GGDD[room_name].paddles, room_name)
        players = []
        for player in GGDD[room_name].paddles:
            players.append(player.toJson())
        await get_channel_layer().group_send(f'game_{room_name}', {'type': 'tick_data', 'P': players, 'Ball': GGDD[room_name].ball.toJson()})
        elapsedTime = time.time() - startTime
        await sleep(elapsedTime, room_name)
    game = await getGameById(room_name)
    game.score = GGDD[room_name].score
    game.endTime = now()
    GameIdEth = requests.post("http://user-management:8000/api/games/add", json=game.toJson()).json()
    game.GameIdEth = GameIdEth["gameId"]
    if game.admin != 0:
        await sync_to_async(game.delete)()
    else:
        await sync_to_async(game.save)()
    await get_channel_layer().group_send(f'game_{room_name}', {"type": "close_connection"})
    await asyncio.sleep(5000)
    del GGDD[room_name]
    