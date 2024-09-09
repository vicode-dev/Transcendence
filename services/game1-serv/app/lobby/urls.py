# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("api/create", views.create, name="create"),
    path("api/start", views.start, name="start")
]