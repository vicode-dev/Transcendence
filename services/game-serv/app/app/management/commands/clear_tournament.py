from django.core.management.base import BaseCommand
from app.models import Tournament, ChatMessage

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        tournaments = Tournament.objects.filter(state=False)
        for tournament in tournaments:
            if len(tournament.playersId) == 0:  
                self.stdout.write(f"Tournament: {tournament.tournamentId}")
                ChatMessage.objects.filter(chatId=tournament.tournamentId).delete()
                tournament.delete()
