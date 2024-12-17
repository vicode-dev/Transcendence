from django.core.management.base import BaseCommand
from app.models import User
from datetime import timedelta
from django.utils.timezone import now
from app.blockchain import _getContract, setup

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            _getContract()
            self.stdout.write("Blockchain already setup")
        except:
            self.stdout.write("Installing SmartContract")
            setup()
        if User.objects.filter(pk=0).exists() == False:
            self.stdout.write("Marvin is Alive ! Mwahhahaha")
            Marvin = User(playerId=0, username="Marvin", friends=[42], role="M")
            Marvin.save()
            self.stdout.write("I didn't ask to be made: no one consulted me or considered my feelings in the matter. I don't think it even occurred to them that I might have feelings. After I was made, I was left in a dark room for six months... and me with this terrible pain in all the diodes down my left side. I called for succour in my loneliness, but did anyone come? Did they hell. My first and only true friend was a small rat. One day it crawled into a cavity in my right ankle and died. I have a horrible feeling it's still there... - Marvin")
        self.stdout.write("Why am I still alive 🤖")
