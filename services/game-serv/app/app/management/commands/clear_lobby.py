from django.core.management.base import BaseCommand
from app.models import Game, ChatMessage
from datetime import timedelta
from django.utils.timezone import now

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        games = Game.objects.filter(state=False)
        timelimit = timedelta(minutes=5)
        for game in games:
            if len(game.players) == 0 and now() - game.startTime  >= timelimit:  
                self.stdout.write(f"Lobby: {game.gameId}")
                ChatMessage.objects.filter(chatId=game.gameId).delete()
                game.delete()
