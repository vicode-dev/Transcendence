# chat/consumers.py
import json
from app.models import Game
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class LobbyConsumer(WebsocketConsumer):
    players_list = ["XXXGamer2005", "DarkWarlock", "girlzz", "vicode"]
    number = 2

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "lobby_%s" % self.room_name
        # if (self.number >= self.max_number):
        #     return
        # Join room group
        data = Game.objects.get(pk=self.room_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        players = self.players_list[:self.number]
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': 'lobby_game', 'players':players, 'maxnumber':data.max_player})
        # self.send(text_data=json.dumps({"players": players, "maxnumber": self.max_number}))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        pass

    def lobby_game(self, event):
        players = event['players']
        maxnumber = event['maxnumber']

        self.send(text_data=json.dumps({
            'type':'lobby_game',
            'players':players,
            'maxnumber':maxnumber,
        }))

    def lobby_redirect(self, event):
        self.send(text_data=json.dumps({
            'type':'lobby_redirect'
        }))