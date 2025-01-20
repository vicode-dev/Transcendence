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
from .Pong import *


class PongConsumer4P(PongConsumer):

    async def connect(self):
        self.scope = self.scope
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"game_{self.room_name}"
        if not await game_exists(self.room_name, 4): # RAJOUTER VERIFICATION DU NOMBRE DE JOUEUR
            await self.close()
        await self.accept()
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await initGameData(self.room_name, 4)
        self.index = await self.get_index()
        if await isPlayerIdInGame(self.room_name, self.scope["token_check"]["id"]):
            if self.scope["token_check"]["id"] not in GGDD[self.room_name].playersId:
                GGDD[self.room_name].playersId.append(self.scope["token_check"]["id"])
        if len(GGDD[self.room_name].playersId) == 4:
            if GGDD[self.room_name].started == False:
                asyncio.create_task(gameLoop(self.room_name, 4, ballMovement))
            elif GGDD[self.room_name].freeze == True:
                await self.channel_layer.group_send(self.room_group_name, {'type': 'freeze', "state": False})
        if GGDD[self.room_name].freeze == True:
            await self.freeze({"type": "freeze", "state": True})

    async def receive(self, text_data):
        try:
            msg = json.loads(text_data)
            if msg["type"] == "move":
                if GGDD[self.room_name].score[self.index] <= 0:
                    pass
                GGDD[self.room_name].playersMove[self.index] = msg["paddleMove"]
            if msg["type"] == 'refresh':
                await self.channel_layer.group_send(self.room_group_name, {'type':'init', 'playersList':GGDD[self.room_name].playersOrder})
        except:
            pass

# [0 for i in range(SIZE)]

def ballReachObstacle(ball, score, p1, p2, p3, p4, x, y):
    if score[0] > 0 and willHitLeftPaddle(ball, p1._x, p1._y, x, y) == True:
        ballHitPlayer(ball, 280, 160, y - p1._y)
        if ball._speed < MAX_SPEED:
            ball._speed += 0.1
    elif score[1] > 0 and willHitRightPaddle(ball, p2._x, p2._y, x, y) == True:
        ballHitPlayer(ball, 260, -160, y - p2._y)
        if ball._speed < MAX_SPEED:
            ball._speed += 0.1
    elif score[2] > 0 and willHitTopPaddle(ball, p3._x, p3._y, x, y) == True:
        ballHitPlayer(ball, 170, -160, x - p3._x)
        if ball._speed < MAX_SPEED:
            ball._speed += 0.1
    elif score[3] > 0 and willHitBottomPaddle(ball, p4._x, p4._y, x, y) == True:
        ballHitPlayer(ball, 190, 160, x - p4._x)
        if ball._speed < MAX_SPEED:
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

def resetAngle(idx, score):
    angles = [180, 0, 270, 90]
    for i in range(idx, idx + 4):
        j = i % 4
        if j != idx and score[j] > 0:
            return angles[j]
    return 0

async def ballMovement(score, ball, players, room_name):
    p1 = players[0]
    p2 = players[1]
    p3 = players[2]
    p4 = players[3]
    if hitWall(ball._x) or hitWall(ball._y):
        playersAreWall = True
        if hitWall(ball._x):
            if score[0] > 0 and ball._x - BALL_SIZE <= 0:
                playersAreWall = False
                ball._angle = resetAngle(0, score) + randomAngle()
                newPoint(score, 0)
                await updateModelScore(room_name, score)
                await get_channel_layer().group_send(f"game_{room_name}",  {'type': 'score_update', "score": score, "angle": ball._angle})
            elif score[1] > 0 and ball._x + BALL_SIZE >= SIZE:
                playersAreWall = False
                ball._angle = resetAngle(1, score) + randomAngle()
                newPoint(score, 1)
                await updateModelScore(room_name, score)
                await get_channel_layer().group_send(f"game_{room_name}",  {'type': 'score_update', "score": score, "angle": ball._angle})
        else:
            if score[2] > 0 and ball._y - BALL_SIZE <= 0:
                playersAreWall = False
                ball._angle = resetAngle(2, score) + randomAngle()
                newPoint(score, 2)
                await updateModelScore(room_name, score)
                await get_channel_layer().group_send(f"game_{room_name}",  {'type': 'score_update', "score": score, "angle": ball._angle})
            elif score[3] > 0 and ball._y + BALL_SIZE >= SIZE:
                playersAreWall = False
                ball._angle = resetAngle(3, score) + randomAngle()
                newPoint(score, 3)
                await updateModelScore(room_name, score)
                await get_channel_layer().group_send(f"game_{room_name}",  {'type': 'score_update', "score": score, "angle": ball._angle})
        if playersAreWall == False:
            ball._x = 4.5
            ball._y = 4.5
            ball._speed = INIT_SPEED
            return
    x = ball._x + (math.cos(math.radians(ball._angle)) / 8) * ball._speed
    y = ball._y + (math.sin(math.radians(ball._angle)) / 8) * ball._speed

    if ballReachObstacle(ball, score, p1, p2, p3, p4, x, y):
        return
    ball._x = x
    ball._y = y
