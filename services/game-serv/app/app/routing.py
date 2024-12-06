# chat/routing.py
from django.urls import re_path

from app.consumers import Pong2P, Pong4P, Connect4

websocket_urlpatterns = [
    re_path(r"ws/game/(?P<room_name>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/2pong", Pong2P.PongConsumer2P.as_asgi()),
    re_path(r"ws/game/(?P<room_name>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/4pong", Pong4P.PongConsumer4P.as_asgi()),
    re_path(r"ws/game/(?P<room_name>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/connect4", Connect4.ConnectConsumer.as_asgi()),
]