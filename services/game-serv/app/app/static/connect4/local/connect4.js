const COLUMNS = 7
const ROWS = 6
const RED = 1
const YELLOW = 2

const COLOR = ["black", "green"] // accentColor crash
const board = new Array(ROWS);
for (let i = 0; i < ROWS; i++) {
    board[i] = new Array(COLUMNS).fill(0);
}
let boardState = new Array(COLUMNS).fill(ROWS - 1);
let turn = 0;
let gameOver = 0;

let playerBtn1 = document.getElementById("player-btn-1");
let playerBtn2 = document.getElementById("player-btn-2");
document.getElementById("start-again").style.display = "none";

let player1Score = 0;
let player2Score = 0;
document.getElementById("player1-score").innerHTML = 0;
document.getElementById("player2-score").innerHTML = 0;

startConnect4();

// document.addEventListener('DOMContentLoaded', function () {
function startConnect4() {
    playerBtn1.style.backgroundColor = COLOR[turn];

    let c1 = document.getElementById("c1");
    let c2 = document.getElementById("c2");
    let c3 = document.getElementById("c3");
    let c4 = document.getElementById("c4");
    let c5 = document.getElementById("c5");
    let c6 = document.getElementById("c6");
    let c7 = document.getElementById("c7");

    c1.addEventListener('click', function () {
        dropPiece(0);
    })
    c2.addEventListener('click', function () {
        dropPiece(1);
    })
    c3.addEventListener('click', function () {
        dropPiece(2);
    })
    c4.addEventListener('click', function () {
        dropPiece(3);
    })
    c5.addEventListener('click', function () {
        dropPiece(4);
    })
    c6.addEventListener('click', function () {
        dropPiece(5);
    })
    c7.addEventListener('click', function () {
        dropPiece(6);
    })
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

function dropPiece(col) {
    if (boardState[col] >= 0 && gameOver == 0) {
        board[boardState[col]][col] = turn + 1;
        if (boardFull() == true) {
            gameOver = 1;

            let content = document.getElementById("connect-content");
            const newDiv = document.createElement("div");
            newDiv.setAttribute("class", "mt-3");
            newDiv.innerHTML = "<p>Game has two losers :(</p>";
            content.append(newDiv);
        }
        else if (checkWin(boardState[col], col) == true) {
            gameOver = 2;
            finishGameUpdate();
        }
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

        updatePlayersBtnColor();
    }
}

function boardFull() {
    for (let i = 0; i < COLUMNS; i++) {
        if (boardState[i] >= 0)
            return false;
    }
    return true;
}

function updatePlayersBtnColor() {
    if (turn % 2 == 0) {
        playerBtn1.style.backgroundColor = COLOR[turn];
        playerBtn2.style.backgroundColor = "";
    } else {
        playerBtn2.style.backgroundColor = COLOR[turn];
        playerBtn1.style.backgroundColor = ""; 
    }
}

function finishGameUpdate() {
    let content = document.getElementById("connect-content");
    const newDiv = document.createElement("div");
    content.append(newDiv);

    // startBtn = document.getElementById("start-again").style.display = "block";

    if (turn % 2 == 0)
    {
        newDiv.innerHTML = "<p>Player 1 won!</p>";
        document.getElementById("player1-score").remove();
        
        let newScore = document.createElement("p");
        newScore.setAttribute("id", "player1-score");
        newScore.innerHTML = (player1Score += 1);
        playerBtn1.append(newScore);
    }
    else
    {
        document.getElementById("player2-score").remove();
        
        let newScore = document.createElement("p");
        newScore.setAttribute("id", "player2-score");
        newScore.innerHTML = (player2Score += 1);
        playerBtn2.append(newScore);
    }
}

function newGame() {
    document.getElementById("pieces").remove();
    let newPieces = document.createElement("g");
    newPieces.setAttribute("id", "pieces");
    newPieces.setAttribute("class", "pieces");
    document.getElementById("board").insertBefore(newPieces, document.getElementById("c1")); 
    boardState = new Array(COLUMNS).fill(ROWS - 1);
    turn = 0;
    gameOver = 0;
    startConnect4();
}