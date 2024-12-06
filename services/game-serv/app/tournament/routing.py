from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/tournament/(?P<tournamentId>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$", consumers.TournamentConsumer.as_asgi()),
]