import time, curses, math
from curses import wrapper
TICK_RATE = 1 / 20

class Ball:

    def __init__(self):
        self._x = 50
        self._y = 15
        self._angle = 115

class Player:

    def __init__(self, x, y):
        self._y = y #15
        self._x = x #0

class GameData:

    def __init__(self):
        self._score = [0, 0, 0, 0]

def draw_paddle(stdscr, x, y):
    for i in range(3):
        stdscr.addch(y + i, x, '|')

# Draw the ball
def draw_ball(stdscr, ball_x, ball_y):
    stdscr.addch(ball_y, ball_x, '@')

def ball_movement(gameData, ball, p1, p2):
    x = ball._x + math.cos(math.radians(ball._angle))
    y = ball._y + math.sin(math.radians(ball._angle))
    
    if (p1._y <= y <= p1._y + 3 and x <= p1._x):
        if (p1._y <= y < p1._y + 1):
            ball._angle = 345
        elif (p1._y + 1 < y <= p1._y + 2):
            ball._angle = 15
        else:
            ball._angle = 0

    if (p2._y <= y <= p2._y + 3 and x >= p2._x):
        if (p2._y <= y < p2._y + 1):
            ball._angle = 245
        elif (p2._y + 1 < y <= p2._y + 2):
            ball._angle = 105
        else:
            ball._angle = 180
    x = ball._x + math.cos(math.radians(ball._angle))
    y = ball._y + math.sin(math.radians(ball._angle))

    if (0 < x < 100):
        ball._x = x 
    if (1 < y < 31):
        ball._y = y
    if (x >= 100 or x <= 0):
        if (x <= 0):
            gameData._score[0] += 1
            ball._angle = 180
        else:
            gameData._score[1] += 1
            ball._angle = 0
        ball._x = 50
        ball._y = 15

        # if (ball._angle % 90 == 0):
        #     ball._angle = (ball._angle + 180) % 360
        # elif (0 < ball._angle < 90 or 180 < ball._angle < 270):
        #     ball._angle = (ball._angle + 90) % 360
        # else:
        #     ball._angle = (360 + ball._angle - 90) % 360
    elif (y <= 1 or y >= 31):
        if (ball._angle % 90 == 0):
            ball._angle = (ball._angle + 180) % 360
        elif (0 < ball._angle < 90 or 180 < ball._angle < 270):
            ball._angle = (360 + ball._angle - 90) % 360
        else:
            ball._angle = (ball._angle + 90) % 360

def gameLoop(stdscr):
    p1 = Player(1, 15)
    p2 = Player(100, 15)
    ball = Ball()
    gameData = GameData()
    stdscr.keypad(True)
    stdscr.timeout(100)
    stdscr.nodelay(True)
    stdscr.border('#')
    
    while True:
        startTime = time.time()
        stdscr.clear()
        stdscr.border()
        key = stdscr.getch()
        if key == ord('q'):  # Quit the game
            break
        elif key == curses.KEY_UP and p2._y > 1:
            p2._y -= 1
        elif key == curses.KEY_DOWN and p2._y < 28:
            p2._y += 1
        elif key == ord('w') and p1._y > 1:
            p1._y -= 1
        elif key == ord('s') and p1._y < 28:
            p1._y += 1
        ball_movement(gameData, ball, p1, p2)
        draw_paddle(stdscr, p1._x, p1._y)
        draw_paddle(stdscr, p2._x, p2._y)
        draw_ball(stdscr, int(ball._x), int(ball._y))
        stdscr.refresh()
        elapsedTime = time.time() - startTime
        time.sleep(max(0, TICK_RATE - elapsedTime))
def displayMenu(stdscr):
    stdscr.addstr(0, 1, "New Game")

def main(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    title = "Pong CLI 🏓!"
    stdscr.refresh()
    while True:
        height, width = stdscr.getmaxyx()
        key = stdscr.getch()
        stdscr.addstr(0, height // 2 - (len(title) // 2), title)
        stdscr.refresh()
        if key == ord('q'):  # Quit the game
            break
        if key == ord('n'):
            gameWin = curses.newwin(32, 102, 1, 0)
            gameLoop(gameWin)


# Using the special variable 
# __name__
if __name__=="__main__":
    wrapper(main)


