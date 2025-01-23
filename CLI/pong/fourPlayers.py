from pong.GameClass import Player, Ball, GameData
from pong.utils import SIZE, PADDLE_SIZE, PADDLE_WIDTH, BALL_SIZE, TICK_RATE, MAX_SPEED
import math, curses, time, random

def randomAngle():
    ang = random.randint(-30, 30)
    while (ang == 0):
        ang = random.randint(-30, 30)
    return ang

def willHitLeftPaddle(ball, px, py, x, y):
    if ((x - BALL_SIZE < px + PADDLE_WIDTH and py <= y - BALL_SIZE and y - BALL_SIZE <= py + PADDLE_SIZE)):
        ball._x = px + PADDLE_WIDTH + BALL_SIZE
    elif (x - BALL_SIZE < px + PADDLE_WIDTH and py <= y + BALL_SIZE and y + BALL_SIZE <= py + PADDLE_SIZE):
        ball._x = px + PADDLE_WIDTH + BALL_SIZE
    else:
        return False
    return True

def willHitRightPaddle(ball, px, py, x, y):
    if ((px < x + BALL_SIZE and py <= y + BALL_SIZE and y + BALL_SIZE <= py + PADDLE_SIZE)):
        ball._x = px - PADDLE_WIDTH - BALL_SIZE
    elif ((px < x + BALL_SIZE and py <= y - BALL_SIZE and y - BALL_SIZE <= py + PADDLE_SIZE)):
        ball._x = px - PADDLE_WIDTH - BALL_SIZE
    else:
        return False
    return True

def willHitTopPaddle(ball, px, py, x, y):
    if ((y - BALL_SIZE < py + PADDLE_WIDTH and px <= x - BALL_SIZE and x - BALL_SIZE <= px + PADDLE_SIZE)):
        ball.y = py + PADDLE_WIDTH + BALL_SIZE
    elif ((y - BALL_SIZE < py + PADDLE_WIDTH and px <= x + BALL_SIZE and x + BALL_SIZE <= px + PADDLE_SIZE)):
        ball.y = py + PADDLE_WIDTH + BALL_SIZE
    else:
        return False
    return True

def willHitBottomPaddle(ball, px, py, x, y):
    if ((py < y + BALL_SIZE and px <= x + BALL_SIZE and x + BALL_SIZE <= px + PADDLE_SIZE)):
        ball.y = py - BALL_SIZE
    elif (py < y + BALL_SIZE and px <= x - BALL_SIZE and x - BALL_SIZE <= px + PADDLE_SIZE):
        ball.y = py - BALL_SIZE
    else:
        return False
    return True

def hitWall(x):
    if x - BALL_SIZE <= 0 or x + BALL_SIZE >= SIZE:
        return True
    return False

def willHitWall(x):
    if (x - BALL_SIZE < 0 or x + BALL_SIZE > SIZE):
        return True
    return False

def ballHitPlayer(ball, startAngle, diff, ballPos):
    ball._angle = (360 + startAngle + (diff / (PADDLE_SIZE + 2 * BALL_SIZE)) * (ballPos + BALL_SIZE)) % 360

def newPoint(score, idx):
    score[idx] -= 1
    for i in range(4):
        if i != idx and score[i] <= 0 and score[idx] == 0:
            score[i] -= 1

def ballReachObstacle(ball, score, p1, p2, p3, p4, x, y):
    if score[0] > 0 and willHitLeftPaddle(ball, p1._x, p1._y, x, y) == True:
        ballHitPlayer(ball, 280, 160, y - p1._y)
        ball._speed += 0.1
    elif score[1] > 0 and willHitRightPaddle(ball, p2._x, p2._y, x, y) == True:
        ballHitPlayer(ball, 260, -160, y - p2._y)
        ball._speed += 0.1
    elif score[2] > 0 and willHitTopPaddle(ball, p3._x, p3._y, x, y) == True:
        ballHitPlayer(ball, 170, -160, x - p3._x)
        ball._speed += 0.1
    elif score[3] > 0 and willHitBottomPaddle(ball, p4._x, p4._y, x, y) == True:
        ballHitPlayer(ball, 190, 160, x - p4._x)
        ball._speed += 0.1
    elif willHitWall(x) == True:
        if ball._x < SIZE / 2:
            ball._x = BALL_SIZE
            if score[0] <= 0:
                if ball._angle % 90 == 0:
                    ball._angle = 180 + ball._angle
                else:
                    ball._angle = (360 + 180 - ball._angle) % 360
        else:
            ball._x = SIZE - BALL_SIZE
            if score[1] <= 0:
                if ball._angle % 90 == 0:
                    ball._angle = 180 + ball._angle
                else:
                    ball._angle = (360 + 180 - ball._angle) % 360
    elif willHitWall(y) == True:
        if ball._y < SIZE / 2:
            ball._y = BALL_SIZE
            if score[2] <= 0:
                if ball._angle % 180 == 0:
                    ball._angle = (ball._angle + 180) % 360
                else:
                    ball._angle = 360 - ball._angle
        else:
            ball._y = SIZE - BALL_SIZE
            if score[3] <= 0:
                if ball._angle % 180 == 0:
                    ball._angle = (ball._angle + 180) % 360
                else:
                    ball._angle = 360 - ball._angle
    else:
        return False
    return True

def resetAngle(idx, score):
    angles = [180, 0, 270, 90]
    for i in range(idx, idx + 4):
        j = i % 4
        if j != idx and score[j] > 0:
            return angles[j]
    return 0

def ballMovement(score, ball, p1, p2, p3, p4):
    if hitWall(ball._x) or hitWall(ball._y):
        playersAreWall = True
        if hitWall(ball._x):
            if score[0] > 0 and ball._x - BALL_SIZE <= 0:
                playersAreWall = False
                ball._angle = resetAngle(0, score) + randomAngle()
                newPoint(score, 0)
            elif score[1] > 0 and ball._x + BALL_SIZE >= SIZE:
                playersAreWall = False
                ball._angle = resetAngle(1, score) + randomAngle()
                newPoint(score, 1)
        else:
            if score[2] > 0 and ball._y - BALL_SIZE <= 0:
                playersAreWall = False
                ball._angle = resetAngle(2, score) + randomAngle()
                newPoint(score, 2)
            elif score[3] > 0 and ball._y + BALL_SIZE >= SIZE:
                playersAreWall = False
                ball._angle = resetAngle(3, score) + randomAngle()
                newPoint(score, 3)
        if playersAreWall == False:
            ball._x = 4.5
            ball._y = 4.5
            ball._speed = 1
    x = ball._x + (math.cos(math.radians(ball._angle)) / 8) * ball._speed
    y = ball._y + (math.sin(math.radians(ball._angle)) / 8) * ball._speed

    if ballReachObstacle(ball, score, p1, p2, p3, p4, x, y):
        return
    ball._x = x
    ball._y = y

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
    score1 = str(gameData._score[0]) if gameData._score[0] >= 0 else "0"
    score2 = str(gameData._score[1]) if gameData._score[1] >= 0 else "0"
    score3 = str(gameData._score[2]) if gameData._score[2] >= 0 else "0"
    score4 = str(gameData._score[3]) if gameData._score[3] >= 0 else "0"
    s = "Player 1: " + score1 + " | Player 2: " + score2 \
        + " | Player 3: " + score3 + " | Player 4: " + score4
    pad.addstr(0, 0, s)

def defeat(score):
    count = 0
    win = 0
    for i in range(4):    
        if (score[i] <= 0):
            count += 1
        else:
            win = i
    if (count == 3):
        score[win] = 1
        newPoint(score, win)
        score = [(i * -1) + 1 for i in score]
        return True
    return False

def gameLoop4P(win, stdscr, pad, scale):
    p1 = Player(0, 3.75)
    p2 = Player(8.75, 3.75)
    p3 = Player(3.75, 0)
    p4 = Player(3.75, 8.75)
    ball = Ball(4.25, 4.25)
    gameData = GameData(5)
    stdscr.keypad(True)
    stdscr.timeout(100)
    stdscr.nodelay(True)
    stdscr.border()
    while True:
        if defeat(gameData._score) == True:
            pad.clear()
            if gameData._score[0] == 1:
                pad.addstr(0, 0, "Player 1 won! Congratulations!")
            elif gameData._score[1] == 1:
                pad.addstr(0, 0, "Player 2 won! Congratulations!")
            elif gameData._score[2] == 1:
                pad.addstr(0, 0, "Player 3 won! Congratulations!")
            else:
                pad.addstr(0, 0, "Player 4 won! Congratulations!")
            pad.refresh(0, 0, 0, 0, 2, win.getmaxyx()[1])
            stdscr.nodelay(False)
            key = stdscr.getch()
            if key == ord('q') or key == 27:
                break
            continue
        startTime = time.time()
        stdscr.erase()
        stdscr.border()
        key = stdscr.getch()
        if key == ord('q') or key == 27:
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
        ballMovement(gameData._score, ball, p1, p2, p3, p4)
        if gameData._score[0] > 0 :
            drawVerticalPaddle(stdscr, scale, int((p1._x) * scale) + 1, int((p1._y) * scale) + 1)
        if gameData._score[1] > 0:
            drawVerticalPaddle(stdscr, scale, int((p2._x) * scale) + 1, int(p2._y * scale) + 1)
        if gameData._score[2] > 0:
            drawHorizontalPaddle(stdscr, scale, int((p3._x) * scale) + 1, int((p3._y) * scale) + 1)
        if gameData._score[3] > 0:
            drawHorizontalPaddle(stdscr, scale, int((p4._x) * scale) + 1, int((p4._y) * scale) + 1)
        drawBall(stdscr, int(ball._x * scale) + 1, int(ball._y * scale) + 1)
        drawScore(pad, gameData)
        pad.refresh(0, 0, 0, 0, 2, win.getmaxyx()[1])
        stdscr.refresh()
        elapsedTime = time.time() - startTime
        curses.napms(int(max(0, TICK_RATE - elapsedTime) * 1000))