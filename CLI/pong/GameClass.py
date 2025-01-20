class Ball:

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._angle = 195
        self._speed = 1

class Player:

    def __init__(self, x, y):
        self._y = y
        self._x = x

class GameData:

    def __init__(self, base_score):
        self._score = [base_score, base_score, base_score, base_score]