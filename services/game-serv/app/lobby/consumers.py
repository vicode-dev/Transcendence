# chat/consumers.py
import json
from app.models import Game
from django.db.models import F, Func, Value
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class LobbyConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "lobby_%s" % self.room_name
        # Join room group
        data = Game.objects.get(pk=self.room_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        if self.scope["token_check"]["id"] not in data.players:
            if len(data.players) != data.maxPlayers:
                data.players.append(self.scope["token_check"]["id"])
                data.save()
        self.accept()
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': 'lobby_game', 'players':data.players, 'maxPlayers':data.maxPlayers})
        # self.send(text_data=json.dumps({"players": players, "maxnumber": self.max_number}))

    def disconnect(self, close_code):
        # Leave room group
        # if Game.objects.get(pk=self.room_name):
        if Game.objects.filter(pk=self.room_name).values_list("state", flat=True).first() == False:
            Game.objects.filter(pk=self.room_name).update(
                players=Func(F('players'), Value(self.scope["token_check"]["id"]), function='array_remove')
            )
        data = Game.objects.get(pk=self.room_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': 'lobby_game', 'players':data.players, 'maxPlayers':data.maxPlayers})

    def receive(self, text_data):
        # text_data
        pass

    def lobby_game(self, event):
        players = event['players']
        maxPlayers = event['maxPlayers']
        self.send(text_data=json.dumps({
            'type':'lobby_game',
            'players':players,
            'maxPlayers': maxPlayers,
        }))

    def lobby_redirect(self, event):
        self.send(text_data=json.dumps({
            'type':'lobby_redirect'
        }))