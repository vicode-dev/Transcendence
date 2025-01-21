from pong.GameClass import Player, Ball, GameData
from pong.utils import SIZE, PADDLE_SIZE, PADDLE_WIDTH, BALL_SIZE, TICK_RATE, MAX_SPEED
from pong.Bot import Bot
from websockets.sync.client import connect
from network.config import configLoad
from threading import Thread
import math, curses, time, json

p1 = Player(0, 3.75)
p2 = Player(8.75, 3.75)
ball = Ball(4.25, 4.25)
gameData = GameData(0)
state = True

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

def ballReachObstacle(ball, p1, p2, x, y): 
    if willHitLeftPaddle(ball, p1._x, p1._y, x, y) == True:
        ballHitPlayer(ball, 280, 160, y - p1._y)
        if ball._speed < MAX_SPEED:
            ball._speed += 0.1
    elif willHitRightPaddle(ball, p2._x, p2._y, x, y) == True:
        ballHitPlayer(ball, 260, -160, y - p2._y)
        if ball._speed < MAX_SPEED:
            ball._speed += 0.1
    elif willHitWall(x) == True:
        if ball._x < SIZE / 2:
            ball._x = BALL_SIZE
        else:
            ball._x = SIZE - BALL_SIZE
    elif willHitWall(y) == True:
        if ball._y < SIZE / 2:
            ball._y = BALL_SIZE
        else:
            ball._y = SIZE - BALL_SIZE
        if ball._angle % 180 == 0:
            ball._angle = (ball._angle + 180) % 360
        else:
            ball._angle = 360 - ball._angle
    else:
        return False
    return True

def ballMovement(score, ball, p1, p2):
    if hitWall(ball._x):
        if ball._x - BALL_SIZE <= 0:
            ball._angle = 0
            score[1] += 1
        else:
            ball._angle = 180
            score[0] += 1
        ball._x = 4.5
        ball._y = 4.5
        ball._speed = 1

    x = ball._x + math.cos(math.radians(ball._angle)) / 8 * ball._speed
    y = ball._y + math.sin(math.radians(ball._angle)) / 8 * ball._speed

    if ballReachObstacle(ball, p1, p2, x, y):
        return
    ball._x = x
    ball._y = y

def drawPaddle(stdscr, scale, x, y):
    for i in range(0, math.ceil(1.5 * scale)):
        stdscr.addch(y + i, x, '|')

def drawBall(stdscr, ball_x, ball_y):
    stdscr.addch(ball_y, ball_x, '੦') #curses.color_pair(1)

def drawScore(pad, gameData):
    s1 = "Player 1: " + str(gameData._score[0]) + " | Player 2: " + str(gameData._score[1])
    pad.addstr(0, 0, s1)

def test(jwt, id):
    config = configLoad()
    ssl_context = ssl.create_default_context()
    websocket = connect(f"wss://{config['server']['url']}/ws/game/{id}/2pong", additional_headers={"Cookie": f"session={jwt}"}, ssl=ssl_context, origin=f"https://{config['server']['url']}")
    return websocket

def gameLoop2P(win, stdscr, pad, scale, websocket):
    global state
    global gameData
    global p1
    global p2
    global ball
    stdscr.keypad(True)
    stdscr.timeout(100)
    stdscr.nodelay(True)
    stdscr.border()
    while True:
        key = stdscr.getch()
        if key == ord('q') or key == 27:
            websocket.close()
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
        elif key == ord('w') or key == ord('d') or key == curses.KEY_RIGHT:
            websocket.send(json.dumps({"type":"move", "paddleMove": 1}), text=True)
        elif key == ord('s') or key == ord('a') or key == curses.KEY_LEFT:
            websocket.send(json.dumps({"type":"move", "paddleMove": -1}), text=True)
        if state == True:
            curses.napms(100)
            continue
        if gameData._score[0] == 10 or gameData._score[1] == 10:
            pad.clear()
            if gameData._score[0] == 10:
                pad.addstr(0, 0, "Player 1 won!")
            elif gameData._score[1] == 10:
                pad.addstr(0, 0, "Player 2 won!")
            pad.refresh(0, 0, 0, 0, 2, win.getmaxyx()[1])
            stdscr.nodelay(False)
            key = stdscr.getch()
            if key == ord('q') or key == 27:
                break
            continue
        startTime = time.time()
        stdscr.erase()
        stdscr.border()
        ballMovement(gameData._score, ball, p1, p2)
        drawPaddle(stdscr, scale, int((p1._x) * scale) + 1, int((p1._y) * scale) + 1)
        drawPaddle(stdscr, scale, int((p2._x) * scale) + 1, int(p2._y * scale) + 1)
        drawBall(stdscr, int(ball._x * scale) + 1, int(ball._y * scale) + 1)
        drawScore(pad, gameData)
        pad.refresh(0, 0, 0, 0, 2, win.getmaxyx()[1])
        stdscr.refresh()
        elapsedTime = time.time() - startTime
        curses.napms(int(max(0, TICK_RATE - elapsedTime) * 1000))

def gameWebsocket(jwt, id, websocket):
    global state
    global p1
    global p2
    global ball
    global gameData
    logger = open("ha.txt", "a")
    while True:
        messageStr = websocket.recv()
        message = json.loads(messageStr)
        match message["type"]:
            case "freeze":
                state = message["state"]
            case "tick_data":
                p1._x = message["P"][0]["x"]
                p1._y = message["P"][0]["y"]
                p2._x = message["P"][1]["x"]
                p2._y = message["P"][1]["y"]
                ball._x = message["Ball"]["x"]
                ball._y = message["Ball"]["y"]
                ball._angle = message["Ball"]["angle"]
                ball._speed = message["Ball"]["speed"]
            case "score_update":
                ball._angle = message["angle"]
                gameData._score = message["scores"]
            # case "init":
                # break
            case "game_end":
                break
    logger.write("End of loop\n")
    logger.close()
    return

def launchGame2P(win, id, jwt):
    global state
    height, width = win.getmaxyx()
    height -= 1
    scale = height - (height % (SIZE)) if height < width else width - (width % SIZE)
    scale = int(scale / 10)
    length = (SIZE * scale) + 2
    win.erase()
    win.refresh()
    gameWin = curses.newwin(length, length, 1, int(width / 2 - length / 2))
    pad = curses.newpad(1, width)
    config = configLoad()
    websocket = connect(f"wss://{config['server']['url']}/ws/game/{id}/2pong", additional_headers={"Cookie": f"session={jwt}"}, origin=f"https://{config['server']['url']}")
    thread = Thread(target = gameWebsocket, args = (jwt, id, websocket))
    thread.start()
    gameLoop2P(win, gameWin, pad, scale, websocket)