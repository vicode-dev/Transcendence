from pong.GameClass import Player, Ball, GameData
import math, curses, time
SIZE = 9
PADDLE_SIZE = 1.5
PADDLE_WIDTH = 0.25
BALL_SIZE = 0.25
TICK_RATE = 1 / 20

def hitPlayer(px, py, x, y):
    if (px <= x - BALL_SIZE <= px + PADDLE_WIDTH and py <= y - BALL_SIZE <= py + PADDLE_SIZE) \
        or (px <= x + BALL_SIZE <= px + PADDLE_WIDTH and py <= y + BALL_SIZE <= py + PADDLE_SIZE) \
        or (px <= x + BALL_SIZE <= px + PADDLE_WIDTH and py <= y - BALL_SIZE <= py + PADDLE_SIZE) \
        or (px <= x - BALL_SIZE <= px + PADDLE_WIDTH and py <= y + BALL_SIZE <= py + PADDLE_SIZE):
        return True
    return False

def ballHitPlayer (ball, startAngle, diff, ballPos):
    ball._angle = (360 + startAngle + (diff / PADDLE_SIZE) * ballPos) % 360

def ballMovement(gameData, ball, p1, p2, p3, p4):
    x = ball._x + math.cos(math.radians(ball._angle)) / 8
    y = ball._y + math.sin(math.radians(ball._angle)) / 8
    
    if hitPlayer(p1._x, p1._y, x, y) == True:
        ballHitPlayer(ball, 280, 160, y - p1._y)
    elif hitPlayer(p2._x, p2._y, x, y) == True:
        ballHitPlayer(ball, 260, -160, y - p2._y)
    elif hitPlayer(p3._y, p3._x, y, x) == True:
        ballHitPlayer(ball, 170, -160, x - p3._x)
    elif hitPlayer(p4._y, p4._x, y, x) == True:
        ballHitPlayer(ball, 190, 160, x - p4._x)
    
    x = ball._x + math.cos(math.radians(ball._angle)) / 8
    y = ball._y + math.sin(math.radians(ball._angle)) / 8
    if (0 < x < SIZE): 
        ball._x = x 
    if (0 < y < SIZE):
        ball._y = y
    if (x >= SIZE or x <= 0):
        if (x <= 0):
            gameData._score[0] -= 1
            ball._angle = 0
        else:
            gameData._score[1] -= 1
            ball._angle = 180
        ball._x = 4.25
        ball._y = 4.25

    elif (y <= 0 or y >= SIZE):
        if (y <= 0):
            gameData._score[2] -= 1
            ball._angle = 90
        else:
            gameData._score[3] -= 1
            ball._angle = 270
        ball._x = 4.25
        ball._y = 4.25

def drawVerticalPaddle(stdscr, scale, x, y):
    for i in range(0, math.floor(1.5 * scale)):
        stdscr.addch(y + i, x, '|')

def drawHorizontalPaddle(stdscr, scale, x, y):
    for i in range(0, math.floor(1.5 * scale)):
        stdscr.addch(y, x + i, '-')

def drawBall(stdscr, ball_x, ball_y):
    stdscr.addch(ball_y, ball_x, '੦') #curses.color_pair(1)

def drawScore(pad, gameData):
    pad.erase()
    s = "Player 1: " + str(gameData._score[0]) + " | Player 2: " + str(gameData._score[1]) \
        + " | Player 3: " + str(gameData._score[2]) + " | Player 4: " + str(gameData._score[3])
    pad.addstr(0, 0, s)

def gameLoop4P(win, stdscr, pad, scale):
    p1 = Player(0, 3.75)
    p2 = Player(8.75, 3.75)
    p3 = Player(3.75, 0)
    p4 = Player(3.75, 8.75)
    ball = Ball(4.25, 4.25)
    gameData = GameData(10)
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
            stdscr.mvwin(1, int(width / 2 - length / 2))
            win.refresh()
        elif key == ord('w') and p1._y > PADDLE_WIDTH:
            p1._y -= 0.25
        elif key == ord('s') and p1._y < SIZE - PADDLE_SIZE - PADDLE_WIDTH:
            p1._y += 0.25
        elif key == curses.KEY_UP and p2._y > PADDLE_WIDTH:
            p2._y -= 0.25
        elif key == curses.KEY_DOWN and p2._y < SIZE - PADDLE_SIZE - PADDLE_WIDTH:
            p2._y += 0.25
        elif key == ord('a') and p3._x > PADDLE_WIDTH:
            p3._x -= 0.25
        elif key == ord('d') and p3._x < SIZE - PADDLE_WIDTH - PADDLE_SIZE:
            p3._x += 0.25
        elif key == curses.KEY_LEFT and p4._x > PADDLE_WIDTH:
            p4._x -= 0.25
        elif key == curses.KEY_RIGHT and p4._x < SIZE - PADDLE_WIDTH - PADDLE_SIZE:
            p4._x += 0.25
        ballMovement(gameData, ball, p1, p2, p3, p4)
        drawVerticalPaddle(stdscr, scale, int((p1._x) * scale) + 1, int((p1._y) * scale) + 1)
        drawVerticalPaddle(stdscr, scale, int((p2._x) * scale) + 1, int(p2._y * scale) + 1)
        drawHorizontalPaddle(stdscr, scale, int((p3._x) * scale) + 1, int((p3._y) * scale) + 1)
        drawHorizontalPaddle(stdscr, scale, int((p4._x) * scale) + 1, int((p4._y) * scale) + 1)
        drawBall(stdscr, int(ball._x * scale) + 1, int(ball._y * scale) + 1)
        drawScore(pad, gameData)
        pad.refresh(0, 0, 0, 0, 1, SIZE * scale)
        stdscr.refresh()
        elapsedTime = time.time() - startTime
        curses.napms(int(max(0, TICK_RATE - elapsedTime) * 1000))