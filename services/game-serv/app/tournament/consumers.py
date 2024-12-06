# chat/consumers.py
import json
from app.models import Tournament, Game
from django.db.models import F, Func, Value
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class TournamentConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["tournamentId"]
        self.room_group_name = f"tournament_{self.room_name}"
        # Join room group
        data = Tournament.objects.get(pk=self.room_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        if Tournament.state == True:
            self.reconnect(data)
        else:
            self.connect_lobby(data)
    
    def connect_lobby(self, data):
        if self.scope["token_check"]["id"] not in data.playersId:
            data.playersId.append(self.scope["token_check"]["id"])
            data.save()
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': 'stats', 'players':data.playersId})
        return
    
    def reconnect(self, data):
        return
    
    def disconnect(self, close_code):
        # Leave room group
        # if Game.objects.get(pk=self.room_name):
        if Game.objects.filter(pk=self.room_name).values_list("state", flat=True).first() == False:
            Game.objects.filter(pk=self.room_name).update(
                players=Func(F('players'), Value(self.scope["token_check"]["id"]), function='array_remove')
            )
        data = Game.objects.get(pk=self.room_name)
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': 'stats', 'players':data.players})
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        pass

    def stats(self, event):
        players = event['players']
        self.send(text_data=json.dumps({
            'type':'stats',
            'players':players,
        }))

    def redirect(self, event):
        self.send(text_data=json.dumps({
            'type':'redirect',
            'url': f"/tournament/{event["url"]}"
        }))