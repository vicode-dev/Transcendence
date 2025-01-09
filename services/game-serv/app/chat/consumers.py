# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from app.models import ChatMessage

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # print("Chat has new user\n")
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        msg = json.loads(text_data)
        if msg["type"] == "message":
            message = msg["message"]
            if len(message) > 500:
                message = message[:500]
            dbmessage = ChatMessage(chatId=self.room_name, playerId=self.scope["token_check"]["id"], content=message)
            dbmessage.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "message", "timestamp": dbmessage.time.isoformat(), "content": message, "playerId": self.scope["token_check"]["id"] }
            )
        elif msg["type"] == "history":
            self.history()

    def history(self):
        messages = reversed(ChatMessage.objects.filter(chatId=self.room_name).order_by('-time')[:20])
        for message in messages:
            self.send(text_data=json.dumps({"type": "message", "content": message.content, "timestamp": message.time.isoformat(), "playerId":message.playerId}))
    
    # Receive message from room group
    def message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": "message", "content": event["content"], "playerId": event["playerId"], "timestamp": event["timestamp"]}))