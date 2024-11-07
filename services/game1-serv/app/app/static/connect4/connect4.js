const COLUMNS = 7
const ROWS = 6
const RED = 1
const YELLOW = 2
const COLOR = ["red", "yellow"]
const board = new Array(ROWS);
for (let i = 0; i < ROWS; i++) {
        board[i] = new Array(COLUMNS).fill(0);
    }
const boardState = new Array(COLUMNS).fill(ROWS - 1);
let turn = 0;
let gameOver = 0;

document.addEventListener('DOMContentLoaded', function() {
    let c1 = document.getElementById("c1");
    let c2 = document.getElementById("c2");
    let c3 = document.getElementById("c3");
    let c4 = document.getElementById("c4");
    let c5 = document.getElementById("c5");
    let c6 = document.getElementById("c6");
    let c7 = document.getElementById("c7");

    c1.addEventListener('click', function() {
        dropPiece(0);
    })
    c2.addEventListener('click', function() {
        dropPiece(1);
    })
    c3.addEventListener('click', function() {
        dropPiece(2);
    })
    c4.addEventListener('click', function() {
        dropPiece(3);
    })
    c5.addEventListener('click', function() {
        dropPiece(4);
    })
    c6.addEventListener('click', function() {
        dropPiece(5);
    })
    c7.addEventListener('click', function() {
        dropPiece(6);
    })
})

function checkWin(x, y) {
    let piece = board[x][y];

    for (let c = 0; c < COLUMNS - 3; c++) {
        for (let r = 0; r < ROWS; r++) {
            if (board[r][c] == piece && board[r][c+1] == piece && board[r][c+2] == piece && board[r][c+3] == piece)
                return true;
        }
    }

    for (let c = 0; c < COLUMNS; c++) {
        for (let r = 0; r < ROWS - 3; r++) { 
            if (board[r][c] == piece && board[r+1][c] == piece && board[r+2][c] == piece && board[r+3][c] == piece)
                return true;
        }
    }

    for (let c = 0; c < COLUMNS - 3; c++) {
        for (let r = 0; r < ROWS - 3; r++) {
            if (board[r][c] == piece && board[r+1][c+1] == piece && board[r+2][c+2] == piece && board[r+3][c+3] == piece)
                return true;
        }
    }

    for (let c = 0; c < COLUMNS - 3; c++) {
        for (let r = 3; r < ROWS; r++) {
            if (board[r][c] == piece && board[r-1][c+1] == piece && board[r-2][c+2] == piece && board[r-3][c+3] == piece)
                return true;
        }
    }
    return false;
}

function dropPiece(col) {
    if (boardState[col] >= 0 && gameOver == 0) {
        board[boardState[col]][col] = turn + 1;
        if (boardFull() == true)
            gameOver = 1;
        else if (checkWin(boardState[col], col) == true)
            gameOver = 2;
        let svg = document.getElementById("pieces");
        let piece = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        piece.setAttribute("r", 20);
        piece.setAttribute("fill", COLOR[turn]);
        piece.setAttribute("cx", 25 + 50 * col);
        piece.setAttribute("cy", 25 + boardState[col] * 50);
        piece.setAttribute("class", "Piece");
        svg.appendChild(piece);
        boardState[col] -= 1;
        turn = (turn + 1) % 2;
        console.log(board);
    }
}

function boardFull() {
    for (let i = 0; i < COLUMNS; i++) {
        if (boardState[i] >= 0)
            return false;
    }
    return true;
}
