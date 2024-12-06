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

class PongConsumer2P(PongConsumer):

    async def connect(self):
        self.scope = self.scope
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"game_{self.room_name}"
        if not await game_exists(self.room_name, 2): # RAJOUTER VERIFICATION DU NOMBRE DE JOUEUR
            await self.close()
        await self.accept()
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await initGameData(self.room_name, 2)
        self.index = await self.get_index()
        if await isPlayerIdInGame(self.room_name, self.scope["token_check"]["id"]):
            if self.scope["token_check"]["id"] not in GGDD[self.room_name].playersId:
                GGDD[self.room_name].playersId.append(self.scope["token_check"]["id"])
        if len(GGDD[self.room_name].playersId) == 2:
            if GGDD[self.room_name].started == False:
                asyncio.create_task(gameLoop(self.room_name, 2, ballMovement))
            elif GGDD[self.room_name].freeze == True:
                await self.channel_layer.group_send(self.room_group_name, {'type': 'freeze', "state": False})
        if GGDD[self.room_name].freeze == True:
            await self.freeze({"type": "freeze", "state": True})

    async def receive(self, text_data):
        try:
            msg = json.loads(text_data)
            if msg["type"] == "move":
                GGDD[self.room_name].playersMove[self.index] = msg["paddleMove"]
        except:
            pass


def ballReachObstacle(ball, p1, p2, x, y): 
    if willHitLeftPaddle(ball, p1._x, p1._y, x, y) == True:
        ballHitPlayer(ball, 280, 160, y - p1._y)
        if ball._speed < MAX_SPEED:
            ball._speed += 0.1
    elif willHitRightPaddle(ball, p2._x, p2._y, x, y) == True:
        ballHitPlayer(ball, 260, -160, y - p2._y)
        if ball._speed < MAX_SPEED:
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

async def ballMovement(score, ball, players, room_name):
    p1 = players[0]
    p2 = players[1]
    if hitWall(ball._x):
        if ball._x - BALL_SIZE <= 0:
            ball._angle = 0
            score[1] += 1
            await updateModelScore(room_name, score)
            await get_channel_layer().group_send(f"game_{room_name}",  {'type': 'score_update', "score": score})
        else:
            ball._angle = 180
            score[0] += 1
            await updateModelScore(room_name, score)
            await get_channel_layer().group_send (f"game_{room_name}", {'type': 'score_update', "score": score})
        ball._x = 4.5
        ball._y = 4.5
        ball._speed = 1

    x = ball._x + math.cos(math.radians(ball._angle)) / 8 * ball._speed
    y = ball._y + math.sin(math.radians(ball._angle)) / 8 * ball._speed

    if ballReachObstacle(ball, p1, p2, x, y):
        return
    ball._x = x
    ball._y = y
