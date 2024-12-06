import json, time, math
import asyncio
from app.models import Game
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.utils.timezone import now
from asgiref.sync import sync_to_async

GGDD = {} #Global Game Data Dictionary
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
        if len(GGDD[self.room_name].playersId) == 4:
            if GGDD[self.room_name].started == False:
                asyncio.create_task(gameLoop4P(self.room_name))
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
                if GGDD[self.room_name].score[self.index] <= 0:
                    pass
                GGDD[self.room_name].playersMove[self.index] = msg["paddleMove"]
        except:
            pass
    
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
            'P1':event["P1"],
            'P2': event["P2"],
            'P3': event["P3"],
            'P4': event["P4"],
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
        winner = 0
        for i in range(len(GGDD[self.room_name].score)):
            if GGDD[self.room_name].score[i] == 0:
                winner = i
                break
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

    def __init__(self, playersOrder):
        self.score = [5, 5, 5, 5]
        self.ball = Ball(4.5, 4.5)
        self.paddles = [Player(0, 3.75), Player(8.75, 3.75),  Player(3.75, 0), Player(3.75, 8.75)]
        self.playersOrder = playersOrder
        self.playersId = []
        self.playersMove = [0, 0, 0, 0]
        self.started = False
        self.freeze = False

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
    return Game.objects.filter(pk=room_name, gameType=False, maxPlayers=4).exists()

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

def ballHitPlayer (ball, startAngle, diff, ballPos):
    ball._angle = (360 + startAngle + (diff / (PADDLE_SIZE + 2 * BALL_SIZE)) * (ballPos + BALL_SIZE)) % 360

def ballHitWall(x):
    if x - BALL_SIZE <= 0 or x + BALL_SIZE >= SIZE:
        return True
    return False

def willHitWall(x):
    if (x - BALL_SIZE < 0 or x + BALL_SIZE > SIZE):
        return True
    return False

def ballReachObstacle(ball, score, p1, p2, p3, p4, x, y):
    if score[0] > 0 and willHitLeftPaddle(ball, p1._x, p1._y, x, y) == True:
        ballHitPlayer(ball, 280, 160, y - p1._y)
        ball._speed += 0.1
    elif score[1] > 0 and willHitRightPaddle(ball, p2._x, p2._y, x, y) == True:
        ballHitPlayer(ball, 260, -160, y - p2._y)
        ball._speed += 0.1
    elif score[2] > 0 and willHitTopPaddle(ball, p3._x, p3._y, x, y) == True:
        ballHitPlayer(ball, 170, -160, x - p3._x)
        ball._speed += 0.1
    elif score[3] > 0 and willHitBottomPaddle(ball, p4._x, p4._y, x, y) == True:
        ballHitPlayer(ball, 190, 160, x - p4._x)
        ball._speed += 0.1
    elif willHitWall(x) == True:
        if ball._x < SIZE / 2:
            ball._x = BALL_SIZE
            if score[0] <= 0:
                if ball._angle % 90 == 0:
                    ball._angle = 180 + ball._angle
                else:
                    ball._angle = (360 + 180 - ball._angle) % 360
        else:
            ball._x = SIZE - BALL_SIZE
            if score[1] <= 0:
                if ball._angle % 90 == 0:
                    ball._angle = 180 + ball._angle
                else:
                    ball._angle = (360 + 180 - ball._angle) % 360
    elif willHitWall(y) == True:
        if ball._y < SIZE / 2:
            ball._y = BALL_SIZE
            if score[2] <= 0:
                if ball._angle % 180 == 0:
                    ball._angle = (ball._angle + 180) % 360
                else:
                    ball._angle = 360 - ball._angle
        else:
            ball._y = SIZE - BALL_SIZE
            if score[3] <= 0:
                if ball._angle % 180 == 0:
                    ball._angle = (ball._angle + 180) % 360
                else:
                    ball._angle = 360 - ball._angle
    else:
        return False
    return True

def newPoint(score, idx):
    score[idx] -= 1
    for i in range(4):
        if i != idx and score[i] <= 0 and score[idx] == 0:
            score[i] -= 1

def resetAngle(idx, score):
    angles = [180, 0, 270, 90]
    for i in range(idx, idx + 4):
        j = i % 4
        if j != idx and score[j] > 0:
            return angles[j]
    return 0

async def ballMovement(score, ball, room_name, p1, p2, p3, p4):
    if ballHitWall(ball._x) or ballHitWall(ball._y):
        playersAreWall = True
        if ballHitWall(ball._x):
            if score[0] > 0 and ball._x - BALL_SIZE <= 0:
                playersAreWall = False
                ball._angle = resetAngle(0, score)
                newPoint(score, 0)
                await get_channel_layer().group_send(f"game_{room_name}",  {'type': 'score_update', "score": score})
            elif score[1] > 0 and ball._x + BALL_SIZE >= SIZE:
                playersAreWall = False
                ball._angle = resetAngle(1, score)
                newPoint(score, 1)
                await get_channel_layer().group_send(f"game_{room_name}",  {'type': 'score_update', "score": score})
        else:
            if score[2] > 0 and ball._y - BALL_SIZE <= 0:
                playersAreWall = False
                ball._angle = resetAngle(2, score)
                newPoint(score, 2)
                await get_channel_layer().group_send(f"game_{room_name}",  {'type': 'score_update', "score": score})
            elif score[3] > 0 and ball._y + BALL_SIZE >= SIZE:
                playersAreWall = False
                ball._angle = resetAngle(3, score)
                newPoint(score, 3)
                await get_channel_layer().group_send(f"game_{room_name}",  {'type': 'score_update', "score": score})
        if playersAreWall == False:
            ball._x = 4.5
            ball._y = 4.5
            ball._speed = 1
    x = ball._x + math.cos(math.radians(ball._angle)) / 8
    y = ball._y + math.sin(math.radians(ball._angle)) / 8

    if ballReachObstacle(ball, score, p1, p2, p3, p4, x, y):
        return
    ball._x = x
    ball._y = y

async def sleep(elapsedTime, room_name):
    await asyncio.sleep(max(0, TICK_RATE - elapsedTime))
    timeout = int(time.time())
    while GGDD[room_name].freeze == True:
        await asyncio.sleep(TICK_RATE)
        if int(time.time()) - timeout == 60:
            GGDD[room_name].score = [0,0,0,0]
            break
    
def paddleMove(room_name):
    for i in range(len(GGDD[room_name].playersMove)):
        match GGDD[room_name].playersMove[i]:
            case 1:
                if (i < 2 and GGDD[room_name].paddles[i]._y < SIZE - PADDLE_SIZE - PADDLE_WIDTH):
                    GGDD[room_name].paddles[i]._y += 0.25
                elif i >= 2 and GGDD[room_name].paddles[i]._x < SIZE - PADDLE_SIZE - PADDLE_WIDTH:
                    GGDD[room_name].paddles[i]._x += 0.25
            case -1:
                if i < 2 and GGDD[room_name].paddles[i]._y > PADDLE_WIDTH:
                    GGDD[room_name].paddles[i]._y -= 0.25
                elif i >= 2 and GGDD[room_name].paddles[i]._x > PADDLE_WIDTH:
                    GGDD[room_name].paddles[i]._x -= 0.25
        GGDD[room_name].playersMove[i] = 0

def defeat(score):
    count = 0
    win = 0
    for i in range(4):    
        if (score[i] <= 0):
            count += 1
        else:
            win = i
        if (count == 3):
            score[win] -= score[win] - 1
            newPoint(score, win)
            score = [i * -1 for i in score]
            return True
    return False

async def gameLoop4P(room_name):
    GGDD[room_name].started = True
    await get_channel_layer().group_send(
        f'game_{room_name}',
        {
            'type': 'freeze',
            'state': False
        }
    )
    await asyncio.sleep(3)
    game = await getGameById(room_name)
    game.startTime = now()
    sync_to_async(game.save)()
    index = 0
    while not GGDD[room_name].freeze:
        startTime = time.time()
        if defeat(GGDD[room_name].score) == True:
            await get_channel_layer().group_send(f'game_{room_name}', {'type': 'game_end'})
            break
        paddleMove(room_name)
        # await get_channel_layer().group_send(f'game_{room_name}', {'type': 'tick_data', 'P1': GGDD[room_name].paddles[0].toJson(), 'P2': GGDD[room_name].paddles[1].toJson(), 'P3': GGDD[room_name].paddles[2].toJson(), 'P4': GGDD[room_name].paddles[3].toJson(), 'Ball': GGDD[room_name].ball.toJson()})
        await ballMovement(GGDD[room_name].score, GGDD[room_name].ball, room_name, GGDD[room_name].paddles[0], GGDD[room_name].paddles[1], GGDD[room_name].paddles[2], GGDD[room_name].paddles[3])
        if index % 10 == 0:
            await get_channel_layer().group_send(f'game_{room_name}', {'type': 'tick_data', 'P1': GGDD[room_name].paddles[0].toJson(), 'P2': GGDD[room_name].paddles[1].toJson(), 'P3': GGDD[room_name].paddles[2].toJson(), 'P4': GGDD[room_name].paddles[3].toJson(), 'Ball': GGDD[room_name].ball.toJson()})
            index = 0
        index += 1
        elapsedTime = time.time() - startTime
        await sleep(elapsedTime, room_name)
    game = await getGameById(room_name)
    game.score = GGDD[room_name].score
    game.endTime = now()
    # requests.post("http://user-management:8000/api/games/add", json=game.toJson())
    await sync_to_async(game.delete)()
    await get_channel_layer().group_send(f'game_{room_name}', {"type": "close_connection"})
    await asyncio.sleep(5000)
    del GGDD[room_name]
# dwa