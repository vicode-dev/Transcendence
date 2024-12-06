from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    USER_ROLES = {"MEMBER": "D", "MODERATOR": "M", "ADMIN": "A"}
    playerId=models.PositiveIntegerField(primary_key=True)
    username=models.CharField(max_length=100)
    # profilePicture=models.CharField()
    # profilePicture=models.ImageField() #upload_to='static/profile_picture/'
    # birthdate=models.DateFile()
    eloPong=models.PositiveSmallIntegerField(default=400)
    eloConnect=models.PositiveSmallIntegerField(default=400)
    friends=ArrayField(models.PositiveIntegerField(), default=[])
    role=models.CharField(choices=USER_ROLES, default=USER_ROLES["MEMBER"])
    theme=ArrayField(models.PositiveIntegerField(), default=[0, 0, 0, 0])

    def json(self):
        return {"id": self.playerId, "username": self.username, "friends": self.friends, "role": self.role, "elo": self.eloPong}
    def __str__(self):
        return username