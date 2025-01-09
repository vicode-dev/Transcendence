const COLUMNS = 7
const ROWS = 6
const RED = 1
const YELLOW = 2
const COLOR = [backgroundColor, accentColor]

let board;
let boardState;
let turn;

function boardFull() {
    for (let i = 0; i < COLUMNS; i++) {
        if (boardState[i] >= 0)
            return false;
    }
    return true;
}

function checkWin(x, y) {
    let piece = board[x][y];

    for (let c = 0; c < COLUMNS - 3; c++) {
        for (let r = 0; r < ROWS; r++) {
            if (board[r][c] == piece && board[r][c + 1] == piece && board[r][c + 2] == piece && board[r][c + 3] == piece)
                return true;
        }
    }

    for (let c = 0; c < COLUMNS; c++) {
        for (let r = 0; r < ROWS - 3; r++) {
            if (board[r][c] == piece && board[r + 1][c] == piece && board[r + 2][c] == piece && board[r + 3][c] == piece)
                return true;
        }
    }

    for (let c = 0; c < COLUMNS - 3; c++) {
        for (let r = 0; r < ROWS - 3; r++) {
            if (board[r][c] == piece && board[r + 1][c + 1] == piece && board[r + 2][c + 2] == piece && board[r + 3][c + 3] == piece)
                return true;
        }
    }

    for (let c = 0; c < COLUMNS - 3; c++) {
        for (let r = 3; r < ROWS; r++) {
            if (board[r][c] == piece && board[r - 1][c + 1] == piece && board[r - 2][c + 2] == piece && board[r - 3][c + 3] == piece)
                return true;
        }
    }
    return false;
}