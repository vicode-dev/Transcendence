from django.db.models import Model, UUIDField, PositiveIntegerField, PositiveSmallIntegerField, DateTimeField, BooleanField, TextField
from django.contrib.postgres.fields import ArrayField
import uuid

class Game(Model):
    gameId = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    players = ArrayField(PositiveIntegerField())
    admin = PositiveIntegerField(default=0)
    score = ArrayField(PositiveSmallIntegerField())
    maxPlayers = PositiveSmallIntegerField(default=2)
    startTime = DateTimeField(auto_now_add=True)
    endTime = DateTimeField(blank=True, null=True)
    gameType = BooleanField(default=0)
    private = BooleanField(default=False)
    state = BooleanField(default=False)
    GameIdEth = PositiveIntegerField(default=None, null=True)

    def toJson(self):
        return {"players": self.players, "score": self.score, "maxPlayers": self.maxPlayers, "gameType": self.gameType, "startTime": int(self.startTime.timestamp()), "endTime": int(self.endTime.timestamp())}

class ChatMessage(Model):
    chatId = UUIDField(editable=False, db_index=True)
    messageId = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = DateTimeField(auto_now_add=True)
    playerId = PositiveIntegerField()
    content = TextField(null=True)

class Tournament(Model):
    tournamentId = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gamesUUID = ArrayField(UUIDField(null=True), default=list)
    gamesId = ArrayField(PositiveIntegerField(null=True))
    playersId = ArrayField(PositiveIntegerField(null=True))
    disconnectedPlayersId = ArrayField(PositiveIntegerField(null=True), default=list)
    state = BooleanField(default=False)

    def toJson(self):
        return {"playersId": self.playersId, "gamesId": self.gamesId}
