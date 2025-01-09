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
    # path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('lobby/', include('lobby.urls'), name='lobby'),
    path('tournament/', include('tournament.urls'), name='tournament'),
    # path('profile/', include('profile.urls'), name='profile'),
    path('game/<uuid:gameId>/', views.game),
    path('game/join/', views.matchmaking_page, name='matchmaking_page'),
    path('game/api/join/', views.matchmaking, name='matchmaking'),
    path('game/local/', views.localgame, name='localgame'),
    # path('game/local/pong/', views.pong, name='local_pong'),
    # path('game/local/connect4/', views.connect4, name='local_connect4'),
    #favicon
    # path('favicon.ico', favicon_view),
    
    # for testing:
    path('game/local/select/', views.game_select, name='game_select'),
    # path('url_list/', views.url_list, name='url_list'), #JSON data
    path('theme/', views.theme, name='theme'),
    # path('theme/', views.theme, name='theme'),

    # path('list_paths/', views.list_paths, name='list_paths'),
    # path('test/', views.test, name='test'),
    # path('tournament', createTournament),
	# path('join/', [function]),
]

# urlpatterns += static('/static/', document_root=settings.STATIC_ROOT)