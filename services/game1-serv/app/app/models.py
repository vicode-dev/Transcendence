from django.db import models
from django.contrib.auth.models import User
import uuid

class Score(models.Model):
    # player_id_0 = models.ManyToMany(Player)
    # player_id_1 = models.ManyToMany(Player)
    # player_id_2 = models.ManyToMany(Player)
    # player_id_3 = models.ManyToMany(Player)
    score_0 = models.PositiveIntegerField(blank=True, null=True)
    score_1 = models.PositiveIntegerField(blank=True, null=True)
    score_2 = models.PositiveIntegerField(blank=True, null=True)
    score_3 = models.PositiveIntegerField(blank=True, null=True)

class Game(models.Model):
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    score = models.OneToOneField(Score, on_delete=models.CASCADE, blank=True, null=True)
    max_player = models.PositiveIntegerField()
    state = models.BooleanField(default=False)


