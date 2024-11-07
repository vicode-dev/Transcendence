import curses, time

COLUMNS = 7
ROWS = 6
RED = 1
YELLOW = 2
COLOR = ['🔴', '🟡']

def debug(j):
    alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    if (0 <= j <= 9):
        return str(j)
    if (9 < j <= 24):
        return alpha[j - 10]
    else:
        return "+"

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

def writePad(pad, turn):
    pad.addstr(0, 0, "Player " + str(turn + 1) + " " + COLOR[turn] + " makes a selection (1 - 7)")

def checkWin(board, x, y):
    piece = board[x][y]
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False

def dropPiece(stdscr, key, board, turn):
    col = int(key - ord('1'))
    for i in range(5, -1, -1):
        if (board[i][col] == 0):
            board[i][col] = turn + 1
            stdscr.addch(i * 2 + 2, col * 3 + 1, COLOR[turn])
            stdscr.refresh()
            if checkWin(board, i, col):
                return turn + 2
            turn = (turn + 1) % 2
            break
    return turn

def boardFull(board):
    for i in range(ROWS):
        for j in range(COLUMNS):
            if board[i][j] == 0:
                return False
    return True

def gameConnectLoop(win, stdscr, pad):
    board = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
    turn = 0
    stdscr.keypad(True)
    stdscr.nodelay(True)
    height, width = win.getmaxyx()
    drawBoard(stdscr, ROWS * 2 + 1, COLUMNS * 3 + 1)
    while True:
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            height, width = win.getmaxyx()
            curses.resize_term(*win.getmaxyx())
            win.refresh()
        elif key == ord('q') or key == 27:
            break
        elif ord('1') <= key <= ord('7'):
            turn = dropPiece(stdscr, key, board, turn)
        if turn > 1:
            pad.addstr(0, 0, "Player " + str(turn - 1) + " won! (Press any key to exit)")
            pad.refresh(0, 0, 0, 0, 2, width)
            # stdscr.getch()
            while stdscr.getch() == -1:
                continue
            break
        if boardFull(board) == True:
            pad.addstr(0, 0, "Board full, it's a draw (press any key to exit)")
            pad.refresh(0, 0, 0, 0, 2, width)
            while stdscr.getch() == -1:
                continue
            break
        writePad(pad, turn)
        pad.refresh(0, 0, 0, 0, 2, width)

