from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/lobby/(?P<room_name>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$", consumers.LobbyConsumer.as_asgi()),
]