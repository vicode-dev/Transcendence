from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    USER_ROLES = {"MEMBER": "Member", "MODERATOR": "Moderator", "ADMIN": "Admin"}
    playerId=models.PositiveIntegerField(primary_key=True)
    username=models.CharField(max_length=100)
    # profilePicture=models.CharField()
    # profilePicture=models.ImageField() #upload_to='static/profile_picture/'
    # birthdate=models.DateFile()
    elo=models.PositiveSmallIntegerField()
    friends=ArrayField(models.PositiveIntegerField())
    role=models.CharField(choices=USER_ROLES, default=USER_ROLES["MEMBER"])

    def json(self):
        return {"id": self.playerId, "username": self.username, "friends": self.friends, "role": self.role}
    def __str__(self):
        return username