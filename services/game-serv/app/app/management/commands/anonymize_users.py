from django.core.management.base import BaseCommand
# from app.models import 
from app.utils.api_users import delete_user
import requests

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        response = requests.get("http://user-management:8000/api/players/rgpd/").json()
        for player in response["ids"]:
            status = delete_user(player)
            if status == True:
                self.stdout.write(f"{player}: anonymized")
            else:
                self.stdout.write(f"{player}: {status}")


