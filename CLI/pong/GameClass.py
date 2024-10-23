class Ball:

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._angle = 180

class Player:

    def __init__(self, x, y):
        self._y = y
        self._x = x

class GameData:

    def __init__(self, base_score):
        self._score = [base_score, base_score, base_score, base_score]