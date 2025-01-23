import curses, json, requests
from connect4.utils import checkWin, boardFull, COLUMNS, ROWS, COLOR, RED, YELLOW
from connect4.Bot import Connect4Bot
from websockets.sync.client import connect
from network.config import configLoad
from threading import Thread

state = True
board = [[-1] * COLUMNS for _ in range(ROWS)]
turn = 0
players = [0, 0, 0]
gameEnd = 0

def drawBoard(stdscr, rows, columns):
    grid = ["─", "│", "┌", "┐", "┬", "└", "├", "┘", "┴", "┤", "┼"]
    stdscr.addstr(0, 0, " 1  2  3  4  5  6  7")
    for i in range(rows):
        for j in range(columns):
            if i == 0 and j == 0:
                stdscr.addch(i + 1, j, grid[2])
            elif i == 0 and j == columns - 1:
                stdscr.addch(i + 1, j, grid[3])
            elif i == rows - 1 and j == 0:
                stdscr.addch(i + 1, j, grid[5])
            elif i == rows - 1 and j == columns - 1:
                stdscr.addch(i + 1, j, grid[7])
            elif i % 2 == 0 and not (j % 3 == 0 or j == columns - 1):
                stdscr.addch(i + 1, j, grid[0])
            elif j % 3 == 0 and not (i % 2 == 0 or i == rows - 1):
                stdscr.addch(i + 1, j, grid[1])
            elif i % 2 == 0 and j == 0:
                stdscr.addch(i + 1, j, grid[6])
            elif i % 2 == 0 and j == columns - 1:
                stdscr.addch(i + 1, j, grid[9])
            elif j % 3 == 0 and i == 0:
                stdscr.addch(i + 1, j, grid[4])
            elif j % 3 == 0 and i == rows - 1:
                stdscr.addch(i + 1, j, grid[8])
            elif j % 3 == 0 and i % 2 == 0:
                stdscr.addch(i + 1, j, grid[10])

def writePad(pad, s, width):
    global players
    pad.clear()
    if (s):
        pad.addstr(0, 0, s)
    else:
        pad.addstr(0, 0, str(players[turn]) + " " + COLOR[(turn + 1) % 2] + " makes a selection (1 - 7)")
    pad.refresh(0, 0, 0, 0, 2, width)

def dropPiece(stdscr, board):
    for j in range(ROWS):
        for i in range(COLUMNS):
            if (board[j][i] == 0 or board[j][i] == 1):
                stdscr.addch(j * 2 + 2, i * 3 + 1, COLOR[board[j][i]])
    stdscr.refresh()


def initPlayers(pList, jwt):
    global players
    config = configLoad()
    for i in range(len(pList)):
        response = requests.get(f"https://{config['server']['url']}/api/player/{pList[i]}/username/", headers={'Cookie': f"session={jwt}"}).json()
        players[i] = response["username"]

def gameWebsocket(jwt, id, websocket):
    global state
    global board
    global turn
    global gameEnd
    while True:
        messageStr = websocket.recv()
        message = json.loads(messageStr)
        match message["type"]:
            case "freeze":
                state = message["state"]
            case "data":
                turn = message["turn"]
                boardState = message["board_state"]
                if boardState[message["col"]] + 1 >= 0:
                    board[boardState[message["col"]] + 1][message["col"]] = turn
            case "start_game":
                initPlayers(message["players"], jwt)
            case "end_game":
                score = message["score"]
                config = configLoad()
                response = requests.get(f"https://{config['server']['url']}/api/player/{message['winner']}/username/", headers={'Cookie': f"session={jwt}"}).json()
                players[2] = response["username"]
                if score[0] == 0 and score[1] == 0:
                    gameEnd = 2
                else:
                    gameEnd = 1
                break
    return



def gameConnectLoop(win, stdscr, pad, websocket):
    global board
    global players
    global turn
    global stdscreen
    stdscreen = stdscr
    stdscr.keypad(True)
    stdscr.nodelay(True)
    height, width = win.getmaxyx()
    drawBoard(stdscr, ROWS * 2 + 1, COLUMNS * 3 + 1)
    while True:
        dropPiece(stdscr, board)
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            height, width = win.getmaxyx()
            curses.resize_term(*win.getmaxyx())
            win.refresh()
        elif key == ord('q') or key == 27:
            break
        elif ord('1') <= key <= ord('7'):  # Human move
            websocket.send(json.dumps({"type":"move", "dropPiece":int(key - ord('1'))}))
        if gameEnd != 0:
            if gameEnd == 1:
                writePad(pad,  str(players[2]) + " won! (press (q) or (esc) to exit)", width)
            if gameEnd == 2:
                writePad(pad, "Board full, it's a draw (press (q) or (esc) to exit)", width)
            stdscr.nodelay(False)
            key = stdscr.getch()
            if key == ord('q') or key == 27:
                break
        writePad(pad, None, width)
        curses.napms(100)


def launchConnectGame(win, id, jwt):
    global pad
    height, width = win.getmaxyx()
    win.erase()
    win.refresh()
    gameWin = curses.newwin(14, 23, 2, int(width / 2 - 23 / 2))
    pad = curses.newpad(1, width)
    config = configLoad()
    websocket = connect(f"wss://{config['server']['url']}/ws/game/{id}/connect4", open_timeout=30, additional_headers={"Cookie": f"session={jwt}"}, origin=f"https://{config['server']['url']}")
    thread = Thread(target = gameWebsocket, args = (jwt, id, websocket))
    thread.start()
    gameConnectLoop(win, gameWin, pad, websocket)
    thread.join()
    return