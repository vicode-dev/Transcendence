import json, time, math
import asyncio
from app.models import Game
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.utils.timezone import now
from asgiref.sync import sync_to_async
import requests
from . import Pong
from .Pong import GGDD

# GGDD = {} #Global Game Data Dictionary
SIZE = 9
PADDLE_SIZE = 1.5
PADDLE_WIDTH = 0.25
BALL_SIZE = 0.125
TICK_RATE = 1 / 20

class PongConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"game_{self.room_name}"
        if not await game_exists(self.room_name): # RAJOUTER VERIFICATION DU NOMBRE DE JOUEUR
            await self.close()
        await self.accept()
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await initGameData(self.room_name)
        self.index = await self.get_index()
        if await isPlayerIdInGame(self.room_name, self.scope["token_check"]["id"]):
            if self.scope["token_check"]["id"] not in GGDD[self.room_name].playersId:
                GGDD[self.room_name].playersId.append(self.scope["token_check"]["id"])
        if len(GGDD[self.room_name].playersId) == 2:
            if GGDD[self.room_name].started == False:
                asyncio.create_task(gameLoop2P(self.room_name))
            elif GGDD[self.room_name].freeze == True:
                await self.channel_layer.group_send(self.room_group_name, {'type': 'freeze', "state": False})
        if GGDD[self.room_name].freeze == True:
            await self.freeze({"type": "freeze", "state": True})

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

    async def receive(self, text_data):
        try:
            msg = json.loads(text_data)
            if msg["type"] == "move":
                GGDD[self.room_name].playersMove[self.index] = msg["paddleMove"]
        except:
            pass

    async def freeze(self, event):
        GGDD[self.room_name].freeze = event["state"]
        players= []
        for player in GGDD[self.room_name].playersOrder:
            if player not in GGDD[self.room_name].playersId:
                players.append(player)
        await self.send(text_data=json.dumps({
            'type':'freeze',
            'state': event["state"],
            'players': players,
        }))
    

    async def tick_data(self, event):
        await self.send(text_data=json.dumps({
            'type':'tick_data',
            'P1':event["P1"],
            'P2': event["P2"],
            'Ball': event["Ball"]
        }))
    
    async def score_update(self, event):
        await self.send(text_data=json.dumps({
            'type':'score_update',
            'scores': event["score"],
        }))

    async def get_index(self):
        for i in range(len(GGDD[self.room_name].playersOrder)):
            if GGDD[self.room_name].playersOrder[i] == self.scope["token_check"]["id"]:
                return i

    async def game_end(self, event):
        winner = 0 if GGDD[self.room_name].score[0] == 10 else 1
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
        self._speed = 1

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

    def __init__(self, _playersOrder):
        self.score = [0, 0]
        self.ball = Ball(4.5, 4.5)
        self.paddles = [Player(0, 3.75), Player(8.75, 3.75)]
        self.playersOrder = _playersOrder
        self.playersId = []
        self.playersMove = [0, 0]
        self.started = False
        self.freeze = True

async def initGameData(room_name):
    if room_name not in GGDD:
        players = await getPlayersIdsInGame(room_name)
        GGDD[room_name] = GameData(players)
    return

@database_sync_to_async
def getPlayersIdsInGame(room_name):
    return Game.objects.filter(pk=room_name).values('players').first()["players"]

@database_sync_to_async
def game_exists(room_name):
    return Game.objects.filter(pk=room_name, gameType=False, maxPlayers=2).exists()

@database_sync_to_async
def isPlayerIdInGame(gameId, playerId):
    return Game.objects.filter(pk=gameId, players__contains=[playerId]).exists() 

@database_sync_to_async
def getGameById(gameId):
	return Game.objects.get(pk=gameId)


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
        ball._x = px - BALL_SIZE
    elif ((px < x + BALL_SIZE and py <= y - BALL_SIZE and y - BALL_SIZE <= py + PADDLE_SIZE)):
        ball._x = px - BALL_SIZE
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

def ballReachObstacle(ball, p1, p2, x, y): 
    if willHitLeftPaddle(ball, p1._x, p1._y, x, y) == True:
        ballHitPlayer(ball, 280, 160, y - p1._y)
        # if ball._speed < 2:
        ball._speed += 0.1
    elif willHitRightPaddle(ball, p2._x, p2._y, x, y) == True:
        ballHitPlayer(ball, 260, -160, y - p2._y)
        # if ball._speed < 2:
        ball._speed += 0.1
    elif willHitWall(x) == True:
        if ball._x < SIZE / 2:
            ball._x = BALL_SIZE
        else:
            ball._x = SIZE - BALL_SIZE
    elif willHitWall(y) == True:
        if ball._y < SIZE / 2:
            ball._y = BALL_SIZE
        else:
            ball._y = SIZE - BALL_SIZE
        if ball._angle % 180 == 0:
            ball._angle = (ball._angle + 180) % 360
        else:
            ball._angle = 360 - ball._angle
    else:
        return False
    return True

async def ballMovement(score, ball, p1, p2, room_name):
    if hitWall(ball._x):
        if ball._x - BALL_SIZE <= 0:
            ball._angle = 0
            score[1] += 1
            await get_channel_layer().group_send(f"game_{room_name}",  {'type': 'score_update', "score": score})
        else:
            ball._angle = 180
            score[0] += 1
            await get_channel_layer().group_send (f"game_{room_name}", {'type': 'score_update', "score": score})
        ball._angle = 0 if ball._x - BALL_SIZE <= 0 else 180
        ball._x = 4.5
        ball._y = 4.5
        ball._speed = 1

    x = ball._x + math.cos(math.radians(ball._angle)) / 8 * ball._speed
    y = ball._y + math.sin(math.radians(ball._angle)) / 8 * ball._speed

    if ballReachObstacle(ball, p1, p2, x, y):
        return
    ball._x = x
    ball._y = y

async def sleep(elapsedTime, room_name):
    await asyncio.sleep(max(0, TICK_RATE - elapsedTime))
    timeout = int(time.time())
    while GGDD[room_name].freeze == True:
        await asyncio.sleep(TICK_RATE)
        if int(time.time()) - timeout == 60:
            GGDD[room_name].score = [0,0]
            break

def paddleMove(room_name):
    for i in range(len(GGDD[room_name].playersMove)):
        match GGDD[room_name].playersMove[i]:
            case 1:
                if (GGDD[room_name].paddles[i]._y < SIZE - PADDLE_SIZE):
                    GGDD[room_name].paddles[i]._y += 0.25
            case -1:
                if GGDD[room_name].paddles[i]._y > 0:
                    GGDD[room_name].paddles[i]._y -= 0.25
        GGDD[room_name].playersMove[i] = 0

async def gameLoop2P(room_name):
    GGDD[room_name].started = True
    await get_channel_layer().group_send(f'game_{room_name}',{'type': 'freeze','state': False}
    )
    await asyncio.sleep(3)
    index = 0
    game = await getGameById(room_name)
    game.startTime = now()
    sync_to_async(game.save)()
    while not GGDD[room_name].freeze:
        startTime = time.time()
        if GGDD[room_name].score[0] == 10 or GGDD[room_name].score[1] == 10:
            # await get_channel_layer().group_send(f'game_{room_name}', {'type': 'freeze','state': True})
            await get_channel_layer().group_send(f'game_{room_name}', {'type': 'game_end'})
            break
        paddleMove(room_name)
        await ballMovement(GGDD[room_name].score, GGDD[room_name].ball, GGDD[room_name].paddles[0], GGDD[room_name].paddles[1], room_name)
        if index % 1 == 0:
            await get_channel_layer().group_send(f'game_{room_name}', {'type': 'tick_data', 'P1': GGDD[room_name].paddles[0].toJson(), 'P2': GGDD[room_name].paddles[1].toJson(), 'Ball': GGDD[room_name].ball.toJson()})
            index = 0
        index += 1
        elapsedTime = time.time() - startTime
        await sleep(elapsedTime, room_name)
    game = await getGameById(room_name)
    game.score = GGDD[room_name].score
    game.endTime = now()
    requests.post("http://user-management:8000/api/games/add", json=game.toJson())
    await sync_to_async(game.delete)()
    await get_channel_layer().group_send(f'game_{room_name}', {"type": "close_connection"})
    await asyncio.sleep(5000)
    del GGDD[room_name]
    