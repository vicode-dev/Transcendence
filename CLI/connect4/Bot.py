import math
from connect4.utils import checkWin, boardFull, COLUMNS, ROWS, RED, YELLOW, COLOR

class Connect4Bot:
    def __init__(self, depth=4):
        # Initialize the bot with a specified search depth
        self.depth = depth

    def score_position(self, board, piece):
        # Scores the current board position for the given piece
        opponent_piece = 2 if piece == 1 else 1
        score = 0

        # Score center column to prioritize central control
        center_column = [board[i][COLUMNS // 2] for i in range(ROWS)]
        center_count = center_column.count(piece)
        score += center_count * 3

        # Score horizontal alignments
        for row in board:
            for col in range(COLUMNS - 3):
                window = row[col:col + 4]
                score += self.evaluate_window(window, piece, opponent_piece)

        # Score vertical alignments
        for col in range(COLUMNS):
            for row in range(ROWS - 3):
                window = [board[row + i][col] for i in range(4)]
                score += self.evaluate_window(window, piece, opponent_piece)

        # Score positively sloped diagonals
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, piece, opponent_piece)

        # Score negatively sloped diagonals
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                window = [board[row - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, piece, opponent_piece)

        return score

    def evaluate_window(self, window, piece, opponent_piece):
        # Evaluate a 4-slot segment (window) for scoring
        score = 0
        if window.count(piece) == 4:
            score += 100  # Prioritize a win condition
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5  # Favor 3 aligned with one empty slot
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2  # Favor 2 aligned with two empty slots

        if window.count(opponent_piece) == 3 and window.count(0) == 1:
            score -= 4  # Penalize opponent's 3 aligned with one empty slot

        return score

    def is_valid_location(self, board, col):
        # Check if a column is valid for a move (not full)
        return board[0][col] == 0

    def get_valid_locations(self, board):
        # Return a list of columns that are valid for a move
        return [col for col in range(COLUMNS) if self.is_valid_location(board, col)]

    def get_next_open_row(self, board, col):
        # Find the next available row in a column
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == 0:
                return row

    def minimax(self, board, depth, alpha, beta, maximizing_player, piece):
        # Minimax algorithm with alpha-beta pruning
        valid_locations = self.get_valid_locations(board)
        is_terminal = checkWin(board, ROWS - 1, 0) or boardFull(board)

        if depth == 0 or is_terminal:
            # Base case: terminal node or depth limit reached
            if is_terminal:
                if checkWin(board, ROWS - 1, 0):
                    # Return a very high/low score for a win/loss condition
                    return (None, 100000000000 if maximizing_player else -100000000000)
                else:
                    return (None, 0)  # Draw scenario
            else:
                # Heuristic score for non-terminal node
                return (None, self.score_position(board, piece))

        if maximizing_player:
            value = -math.inf
            best_col = None
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                temp_board = [r[:] for r in board]  # Copy board
                temp_board[row][col] = piece  # Simulate placing the piece
                new_score = self.minimax(temp_board, depth - 1, alpha, beta, False, piece)[1]
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Prune the branch
            return best_col, value
        else:  # Minimizing player
            value = math.inf
            best_col = None
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                temp_board = [r[:] for r in board]  # Copy board
                temp_board[row][col] = 2 if piece == 1 else 1  # Simulate opponent's move
                new_score = self.minimax(temp_board, depth - 1, alpha, beta, True, piece)[1]
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Prune the branch
            return best_col, value

    def get_move(self, board, piece):
    # Determine the best move for the given piece
        valid_locations = self.get_valid_locations(board)
        best_score = -math.inf
        best_col = None  # Initialize to None for safety

        for col in valid_locations:
            row = self.get_next_open_row(board, col)
            temp_board = [r[:] for r in board]  # Copy board
            temp_board[row][col] = piece  # Simulate placing the piece
            score = self.minimax(temp_board, self.depth - 1, -math.inf, math.inf, False, piece)[1]
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

