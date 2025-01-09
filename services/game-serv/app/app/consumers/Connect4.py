import json, time, math
import asyncio
from app.models import Game
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.utils.timezone import now
import requests

GGDD = {} #Global Game Data Dictionary
COLUMNS = 7
ROWS = 6
RED = 1
YELLOW = 2

class ConnectConsumer(AsyncWebsocketConsumer):

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
            await self.channel_layer.group_send(self.room_group_name, {'type': 'freeze', "state": False})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        if self.scope["token_check"]["id"] in GGDD[self.room_name].playersId:
            GGDD[self.room_name].playersId.remove(self.scope["token_check"]["id"])
            # if GGDD[self.room_name].started == True:
            await self.channel_layer.group_send(self.room_group_name, {'type': 'freeze', "state": True})


    async def receive(self, text_data):
        try:
            msg = json.loads(text_data)
            if msg["type"] == "move" and GGDD[self.room_name].freeze == False:
                if (GGDD[self.room_name].turn == -1):
                    GGDD[self.room_name].turn = self.index
                if (self.index == GGDD[self.room_name].turn):
                    await self.dropPiece(msg['dropPiece'])
            if msg["type"] == "reconnect":
                await self.send(text_data=json.dumps({'type': 'board', 'board':GGDD[self.room_name].board, 'board_state': GGDD[self.room_name].board_state}))
        except:
            pass

    async def data(self, event):
        await self.send(text_data=json.dumps({
            'type':'data',
            'col': event['col'],
            'board_state': event["board_state"],
            'turn': event["turn"],
        }))

    async def freeze(self, event):
        GGDD[self.room_name].freeze = event["state"]
        await self.send(text_data=json.dumps({
            'type':'freeze',
            'state': event["state"],
        }))
    
    async def error(self, event):
        await self.send(text_data=json.dumps({
            'type':'error',
            'err': event['err']
        }))

    async def end_game(self, event):
        await self.send(text_data=json.dumps({
            'type':'end_game',
            'score': event["score"],
        }))

    async def get_index(self):
        for i in range(len(GGDD[self.room_name].playersOrder)):
            if GGDD[self.room_name].playersOrder[i] == self.scope["token_check"]["id"]:
                return i

    async def dropPiece(self, col):
        gameEnded = False
        if (col == -1 or col >= COLUMNS):
            await get_channel_layer().group_send(f"game_{self.room_name}",  {'type': 'error', 'err':"Column out of range"})
            return
        elif (GGDD[self.room_name].board_state[col] >= 0):
            GGDD[self.room_name].board[GGDD[self.room_name].board_state[col]][col] = GGDD[self.room_name].turn + 1
            if checkWin(self.room_name, GGDD[self.room_name].board_state[col], col) == True:
                GGDD[self.room_name].freeze = True
                GGDD[self.room_name].score[self.index] += 1
                gameEnded = True
            GGDD[self.room_name].board_state[col] -= 1
            if (boardFull(self.room_name) == True):
                GGDD[self.room_name].freeze = True
                gameEnded = True
            GGDD[self.room_name].turn = (GGDD[self.room_name].turn + 1) % 2
            GGDD[self.room_name].playersMove = [-1, -1]
            await get_channel_layer().group_send(f"game_{self.room_name}",  {'type': 'data', "col": col, 'board_state': GGDD[self.room_name].board_state, 'turn': GGDD[self.room_name].turn})
        if (gameEnded == True):
            await get_channel_layer().group_send(f"game_{self.room_name}",  {'type': 'end_game', 'score':GGDD[self.room_name].score})
            game = await getGameById(self.room_name)
            game.score = GGDD[self.room_name].score
            game.endTime = now()
            requests.post("http://user-management:8000/api/games/add", json=game.toJson()).json()
            await sync_to_async(game.delete)()
            del GGDD[self.room_name]

class GameData:

    def __init__(self, _playersOrder):
        self.score = [0, 0]
        self.playersOrder = _playersOrder
        self.playersId = []
        self.playersMove = [-1, -1]
        self.started = False
        self.freeze = False
        self.board = [[0] * COLUMNS for _ in range(ROWS)]
        self.board_state = [ROWS - 1] * COLUMNS
        self.turn = -1

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
    return Game.objects.filter(pk=room_name).exists()

@database_sync_to_async
def isPlayerIdInGame(gameId, playerId):
    return Game.objects.filter(pk=gameId, players__contains=[playerId]).exists() 

@database_sync_to_async
def getGameById(gameId):
    return Game.objects.get(pk=gameId)

def boardFull(room_name):
    for i in range(COLUMNS):
        if GGDD[room_name].board_state[i] >= 0:
            return False
    return True

def checkWin(room_name, x, y):
    piece = GGDD[room_name].board[x][y]

    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if GGDD[room_name].board[r][c] == piece and GGDD[room_name].board[r][c + 1] == piece and GGDD[room_name].board[r][c + 2] == piece and GGDD[room_name].board[r][c + 3] == piece:
                return True
    for c in range (COLUMNS):
        for r in range(ROWS - 3):
            if GGDD[room_name].board[r][c] == piece and GGDD[room_name].board[r + 1][c] == piece and GGDD[room_name].board[r + 2][c] == piece and GGDD[room_name].board[r + 3][c] == piece:
                return True
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if GGDD[room_name].board[r][c] == piece and GGDD[room_name].board[r + 1][c + 1] == piece and GGDD[room_name].board[r+ 2][c + 2] == piece and GGDD[room_name].board[r + 3][c + 3] == piece:
                return True
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if GGDD[room_name].board[r][c] == piece and GGDD[room_name].board[r - 1][c + 1] == piece and GGDD[room_name].board[r - 2][c + 2] == piece and GGDD[room_name].board[r - 3][c + 3] == piece:
                return True
    return False

    # del GGDD[room_name]  