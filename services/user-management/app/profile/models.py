from django.db import models
from django.contrib.postgres.fields import ArrayField

def defaultTheme():
    return [10935979,5923722,2961991]


class User(models.Model):
    USER_ROLES = {"MEMBER": "D", "MODERATOR": "M", "ADMIN": "A"}
    playerId=models.PositiveIntegerField(primary_key=True)
    username=models.CharField(max_length=100)
    eloPong=models.PositiveSmallIntegerField(default=400)
    eloConnect=models.PositiveSmallIntegerField(default=400)
    friends=ArrayField(models.PositiveIntegerField(), default=list)
    role=models.CharField(choices=USER_ROLES, default=USER_ROLES["MEMBER"])
    theme=ArrayField(models.PositiveIntegerField(), max_length=3, default=defaultTheme)
    lastConnection=models.DateTimeField(auto_now=True)

    def json(self):
        return {"id": self.playerId, "username": self.username, "friends": self.friends, "role": self.role, "elo": self.eloPong}
    def __str__(self):
        return self.username
