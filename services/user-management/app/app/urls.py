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
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("api/games/setup/", views.setupContract),
    path("api/games/", views.getGamesNumber),
    path("api/add", views.add),
	path('api/games/<int:id>/', views.getGameById),
    path('api/tournament/<int:id>/', views.getTournamentById),
    path('api/player/<int:playerId>/', views.getPlayerById),
    path('api/player/<int:playerId>/games/', views.getPlayerGame),
    path('api/player/<int:playerId>/avatar/', views.playerAvatar),
    path('api/player/<int:playerId>/username/', views.getPlayerUsername),
    path('api/player/<int:playerId>/friends/', views.getPlayerFriends),
    path('api/player/add', views.addplayer),
    path('profile/<int:playerId>/', views.profile),
    path('settings/', views.settings),
    path('login-temp/', views.login)
]
