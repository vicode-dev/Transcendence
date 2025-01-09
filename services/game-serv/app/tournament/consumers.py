# chat/consumers.py
import json, asyncio
from app.models import Tournament, Game
from django.db.models import F, Func, Value
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from tournament.gameManagement import death
import logging
logger = logging.getLogger('app')
class TournamentConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["tournamentId"]
        self.room_group_name = f"tournament_{self.room_name}"
        # Join room group
        data = await sync_to_async(Tournament.objects.get)(pk=self.room_name)
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()
        if data.state == True:
            if self.scope["token_check"]["id"] in data.disconnectedPlayersId:
                data.disconnectedPlayersId.remove(self.scope["token_check"]["id"])
                sync_to_async(data.save)()
            await self.reconnect(data)
        else:
            await self.connect_lobby(data)
    
    async def connect_lobby(self, data):
        if self.scope["token_check"]["id"] not in data.playersId:
            data.playersId.append(self.scope["token_check"]["id"])
            await sync_to_async(data.save)()
        logger.debug(data.playersId)
        await self.channel_layer.group_send(
        f'tournament_{self.room_name}',
        {
            'type': 'stats',
            "players": data.playersId,
            "games": data.gamesUUID,
            "gamesArchive": data.gamesId
        }
    )
        return
    
    async def reconnect(self, data):
        await self.channel_layer.group_send(
        f'tournament_{self.room_name}',
        {
            'type': 'stats',
            "players": data.playersId,
            "games": data.gamesUUID,
            "gamesArchive": data.gamesId
        }
        )
        return
    
    async def disconnect(self, close_code):
        # Leave room group
        data = await sync_to_async(Tournament.objects.get)(pk=self.room_name)
        if data.state == True:
            data.disconnectedPlayersId.append(self.scope["token_check"]["id"])
            await sync_to_async(data.save)()
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        msg = json.loads(text_data)
        if msg["type"] == "reconnect":
            data = await sync_to_async(Tournament.objects.get)(pk=self.room_name)
            await self.reconnect(data)
        if msg["type"] == "apocalypse":
            data = await sync_to_async(Tournament.objects.get)(pk=self.room_name)
            asyncio.create_task(death(data))
        pass

    async def stats(self, event):
        await self.send(text_data=json.dumps({
            'type':'stats',
            'players':event['players'],
            # 'games':event['games'],
            'gamesArchive':event['gamesArchive']
        }))

    async  def redirectOne(self, event):
        if (self.scope["token_check"]["id"] == event["id"]):
            await self.send(text_data=json.dumps({
                'type':'redirect',
                'url': f"/tournament/{event["url"]}"
            }))

    async def redirect(self, event):
        await self.send(text_data=json.dumps({
            'type':'redirect',
            'url': f"/tournament/{event["url"]}"
        }))