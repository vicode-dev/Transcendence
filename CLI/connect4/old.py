import numpy as np
import signal
import sys
import os

COLUMNS = 7
ROWS = 6
errors = 0

def create_board():
    return np.zeros((ROWS, COLUMNS), dtype=int)

def clear_prompt():
    global errors
    for _ in range(errors + 1):
        sys.stdout.write("\033[F")  # Move cursor up one line
        sys.stdout.write("\033[K")  # Clear the line
    errors = 1
    sys.stdout.flush()

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    if col < 1 or col > board.shape[1]:
        return False
    return board[0][col - 1] == 0

def get_next_open_row(board, col):
    for row in range(board.shape[0]):
        if board[row][col - 1] == 0:
            return row

def print_board(board):
    os.system('clear')
    print("\n  1 2 3 4 5 6 7")
    print(" +-------------+")
    for row in range(board.shape[0]):
        print(" |", end="")
        for col in range(board.shape[1]):
            if board[row][col] == 0:
                print("  ", end="")
            elif board[row][col] == 1:
                print("🔴", end="")
            else:
                print("🟡", end="")
        print("|")
    print(" +-------------+")
    global errors
    errors = 0

def signal_handler(sig, frame):
    print("\nGame interrupted. Exiting gracefully...")
    sys.exit(0)

def is_board_full(board):
    return not np.any(board == 0)

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMNS-3):
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

signal.signal(signal.SIGINT, signal_handler)

board = create_board()
game_over = False
turn = 0

print_board(board)
while not game_over:
    try:
        colStr = input("Player " + str(turn + 1) + " make a selection (1-7): ")
        col = int(colStr)

        if is_valid_location(np.flipud(board), col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col - 1, turn + 1)
            print_board(np.flipud(board))
            if winning_move(board, turn + 1):
                print("Player " + str(turn + 1) + " wins!")
                game_over = True
            turn += 1
            turn = turn % 2
        else:
            clear_prompt()
            print("Invalid location. Please choose a column between 1 and 7 that is not full.")
        if is_board_full(board) and not game_over:
            print("Game over. It's a draw!")
            game_over = True
    except EOFError:
        print("\nInput ended. Exiting gracefully...")
        sys.exit(0)
    except ValueError:
        clear_prompt()
        print("Invalid input. Please enter a number between 1 and 7.")