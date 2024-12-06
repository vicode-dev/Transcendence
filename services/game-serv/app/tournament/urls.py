# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="tournament_index"),
    path("<uuid:room_name>/", views.room, name="room"),
    path("api/create", views.create, name="create"),
    path("<uuid:room_name>/start", views.start, name="start"),
    path("<uuid:room_name>/dashboard/", views.dashboard)
]