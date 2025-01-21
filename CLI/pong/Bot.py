import time
from pong.utils import SIZE


class Bot:
    def __init__(self, x,y,paddle_size,max_speed, player):
        self._x = x
        self._y = y
        self._paddle_size = paddle_size
        self._max_speed = max_speed
        self._side = player
        self._last_calculation_time = 0

#add a delay for hte bot to react to the ball
    def get_input(self, ball):
    # Determine movement logic based on the bot's side use -1 to indicate move up and 1 to indicate move down
        current_time = time.time()
        if current_time - self._last_calculation_time < 0.070:
            return 0  # Do nothing if less than 1 second has passed
        self._last_calculation_time = current_time
        paddle_center = self._y + self._paddle_size / 2

        if self._side == "left":
            if ball._x < SIZE / 2 and ball._angle > 90 and ball._angle < 270:
                if ball._y < paddle_center:
                    return -1
                elif ball._y > paddle_center:
                    return 1
        elif self._side == "right":
            if ball._x > SIZE / 2 and (ball._angle < 90 or ball._angle > 270):
                if ball._y < paddle_center:
                    return -1
                elif ball._y > paddle_center:
                    return 1
        elif self._side == "top":
            if ball._y < SIZE / 2 and ball._angle > 0 and ball._angle < 180:
                if ball._x < paddle_center:
                    return -1
                elif ball._x > paddle_center:
                    return 1
        elif self._side == "bottom":
            if ball._y > SIZE / 2 and ball._angle > 180 and ball._angle < 360:
                if ball._x < paddle_center:
                    return -1
                elif ball._x > paddle_center:
                    return 1
        return 0