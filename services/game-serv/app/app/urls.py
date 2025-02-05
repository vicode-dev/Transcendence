"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.singlePage),
    path('chat/', include('chat.urls')),
    path('lobby/', include('lobby.urls'), name='lobby'),
    path('tournament/', include('tournament.urls'), name='tournament'),
    path('game/<uuid:gameId>/', views.game),
    path('game/<uuid:gameId>/api/', views.game_api),
    path('game/join/', views.matchmaking_page, name='matchmaking_page'),
    path('game/api/join/', views.matchmaking, name='matchmaking'),
    path('game/local/', views.localgame, name='localgame'),
    path('game/local/select/', views.game_select, name='game_select'),
    path('theme/', views.theme, name='theme'),
]
