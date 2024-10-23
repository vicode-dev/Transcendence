from pong.GameClass import Player, Ball, GameData
import math, curses, time
SIZE = 9
PADDLE_SIZE = 1.5
BALL_SIZE = 0.25
TICK_RATE = 1 / 20

def ballMovement(gameData, ball, p1, p2):
    x = ball._x + math.cos(math.radians(ball._angle)) / 8
    y = ball._y + math.sin(math.radians(ball._angle)) / 8
    
    if (p1._y <= y <= p1._y + PADDLE_SIZE and x <= p1._x):
        middleLength = PADDLE_SIZE / 2
        middle = p1._y + middleLength
        if (y < middle):
            ball._angle = 360 - ((80 / middleLength) * (middleLength - (y - p1._y)))
        elif (y > middle):
            ball._angle = (80 / middleLength) * (y - middle)
        else:
            ball._angle = 0

    if (p2._y <= y <= p2._y + PADDLE_SIZE and x >= p2._x):
        middleLength = PADDLE_SIZE / 2
        middle = p2._y + middleLength
        if (y < middle):
            ball._angle = 260 - ((80 / middleLength) * ((y - p2._y)))
        elif (y > middle):
            ball._angle = 100 + ((80 / middleLength) * (middleLength - y + middle))
        else:
            ball._angle = 180
    x = ball._x + math.cos(math.radians(ball._angle)) / 8
    y = ball._y + math.sin(math.radians(ball._angle)) / 8
    if (0 < x < SIZE): 
        ball._x = x 
    if (0 < y < SIZE):
        ball._y = y
    if (x >= SIZE or x <= 0):
        if (x <= 0):
            gameData._score[1] += 1
            ball._angle = 0
        else:
            gameData._score[0] += 1
            ball._angle = 180
        ball._x = 4.25
        ball._y = 4.25

    elif (y <= 0 or y >= SIZE):
        if (ball._angle % 90 == 0):
            ball._angle = (ball._angle + 180) % 360
        else:
            ball._angle = 360 - ball._angle

def drawPaddle(stdscr, scale, x, y):
    for i in range(0, math.ceil(1.5 * scale)):
        stdscr.addch(y + i, x, '|')

def drawBall(stdscr, ball_x, ball_y):
    stdscr.addch(ball_y, ball_x, '੦') #curses.color_pair(1)

def drawScore(pad, gameData):
    s1 = "Player 1: " + str(gameData._score[0]) + " | Player 2: " + str(gameData._score[1])
    pad.addstr(0, 0, s1)

def gameLoop2P(win, stdscr, pad, scale):
    p1 = Player(0, 3.75)
    p2 = Player(8.75, 3.75)
    ball = Ball(4.25, 4.25)
    gameData = GameData(0)
    stdscr.keypad(True)
    stdscr.timeout(100)
    stdscr.nodelay(True)
    stdscr.border()
    while True:
        startTime = time.time()
        stdscr.erase()
        stdscr.border()
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_RESIZE:
            win.erase()
            height, width = win.getmaxyx()
            curses.resize_term(*win.getmaxyx())
            scale = height - height % SIZE if height < width else width - width % SIZE
            scale = int(scale / 10)
            length = (SIZE * scale) + 2
            stdscr.resize(length, length)
            stdscr.mvwin(0, int(width / 2 - length / 2))
            win.refresh()
        elif key == curses.KEY_UP and p2._y > 0:
            p2._y -= 0.25
        elif key == curses.KEY_DOWN and p2._y < SIZE - PADDLE_SIZE:
            p2._y += 0.25
        elif key == ord('w') and p1._y > 0:
            p1._y -= 0.25
        elif key == ord('s') and p1._y < SIZE - PADDLE_SIZE:
            p1._y += 0.25
        ballMovement(gameData, ball, p1, p2)
        drawPaddle(stdscr, scale, int((p1._x) * scale) + 1, int((p1._y) * scale) + 1)
        drawPaddle(stdscr, scale, int((p2._x) * scale) + 1, int(p2._y * scale) + 1)
        drawBall(stdscr, int(ball._x * scale) + 1, int(ball._y * scale) + 1)
        drawScore(pad, gameData)
        pad.refresh(0, 0, 0, 0, 2, SIZE * scale)
        stdscr.refresh()
        elapsedTime = time.time() - startTime
        curses.napms(int(max(0, TICK_RATE - elapsedTime) * 1000))