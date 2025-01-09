const COLUMNS = 7
const ROWS = 6
const RED = 1
const YELLOW = 2

// let backgroundColor = window.getComputedStyle(document.documentElement).getPropertyValue('--background-color');
// let secondaryColor = window.getComputedStyle(document.documentElement).getPropertyValue('--secondary-color');
// let accentColor = window.getComputedStyle(document.documentElement).getPropertyValue('--accent-color');

const COLOR = ["black", "green"] // accentColor crash
let board = new Array(ROWS);
for (let i = 0; i < ROWS; i++) {
    board[i] = new Array(COLUMNS).fill(0);
}
let boardState = new Array(COLUMNS).fill(ROWS - 1);
const roomName = getRoomName();
let turn = 0;
let freezeState = false;

startConnect4();

function getRoomName() {
    let url = window.location.href;
    let pathSegments = url.split('/').filter(Boolean);
    return pathSegments[pathSegments.length - 1];
}
// document.addEventListener('DOMContentLoaded', function () {
function startConnect4() {
    let gameWebSocket = new WebSocket(
        'wss://'
        + window.location.host
        + '/ws/game/'
        + roomName
        + '/connect4'
    );
    let c1 = document.getElementById("c1");
    let c2 = document.getElementById("c2");
    let c3 = document.getElementById("c3");
    let c4 = document.getElementById("c4");
    let c5 = document.getElementById("c5");
    let c6 = document.getElementById("c6");
    let c7 = document.getElementById("c7");

    gameWebSocket.addEventListener("message", (event) => {
        msg = JSON.parse(event.data)
        switch (msg.type) {
            case "data":
                UpdateGameData(msg);
                drawPiece(msg["col"]);
                break;
            case "error":
                console.log(msg);
                break;
            case "end_game":
                endGame(msg);
                break;
            case "freeze":
                freeze(msg, gameWebSocket);
                break;
            case "board":
                board = msg["board"];
                boardState = msg["board_state"];
                redraw();
                break;
        }
    });
    gameWebSocket.onopen = function() {
        gameWebSocket.send(JSON.stringify({"type": "reconnect"}));
    }
    // gameWebSocket.onmessage = function(e) {
    //     console.log("Hello world")
    //     redraw();
    // }
    c1.addEventListener('click', function () {
        dropPiece(gameWebSocket, 0);
    })
    c2.addEventListener('click', function () {
        dropPiece(gameWebSocket, 1);
    })
    c3.addEventListener('click', function () {
        dropPiece(gameWebSocket, 2);
    })
    c4.addEventListener('click', function () {
        dropPiece(gameWebSocket, 3);
    })
    c5.addEventListener('click', function () {
        dropPiece(gameWebSocket, 4);
    })
    c6.addEventListener('click', function () {
        dropPiece(gameWebSocket, 5);
    })
    c7.addEventListener('click', function () {
        dropPiece(gameWebSocket, 6);
    })
}

function UpdateGameData(msg) {
    boardState = msg["board_state"];
    turn = msg["turn"];
}

function freeze(msg, gameWebSocket) {
    freezeState = msg["state"];
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

function dropPiece(gameWebSocket, col) {
    if (freezeState == false)
        gameWebSocket.send(JSON.stringify({"type": "move", "dropPiece": col}));
}

function drawPiece(col) {
    if (boardState[col] + 1 >= 0) {
        board[boardState[col] + 1][col] = turn;
        let svg = document.getElementById("pieces");
        let piece = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        piece.setAttribute("r", 20);
        piece.setAttribute("fill", COLOR[(turn + 1) % 2]);
        piece.setAttribute("cx", 25 + 50 * col);
        piece.setAttribute("cy", 25 + (boardState[col] + 1) * 50);
        piece.setAttribute("class", "Piece");
        svg.appendChild(piece);
    }
}

function redraw() {
    for (let i = 0; i < COLUMNS; i++) {
        for (let j = boardState[i] + 1; j < ROWS; j++) {
            let svg = document.getElementById("pieces");
            let piece = document.createElementNS("http://www.w3.org/2000/svg", "circle");
            piece.setAttribute("r", 20);
            piece.setAttribute("fill", COLOR[board[j][i] - 1]);
            piece.setAttribute("cx", 25 + 50 * i);
            piece.setAttribute("cy", 25 + (j) * 50);
            piece.setAttribute("class", "Piece");
            svg.appendChild(piece);
        }
    }
}

function endGame(msg) {
    let score = msg["score"];
    console.log(msg, score);
    freezeState = true;
    if (score[0] == 0 && score[1] == 0) {
        let content = document.getElementById("connect-content");
        const newDiv = document.createElement("div");
        newDiv.setAttribute("class", "mt-3");
        newDiv.innerHTML = "<p>Game has two losers :(</p>";
        content.append(newDiv);
    }
    else {
        let winner = score[0] == 1 ? 0 : 1;
        let content = document.getElementById("connect-content");
        const newDiv = document.createElement("div");
        newDiv.setAttribute("class", "mt-3");
        newDiv.innerHTML = "<p>Player " + (winner + 1) + " has won!</p>";
        content.append(newDiv);
    }
}

function boardFull() {
    for (let i = 0; i < COLUMNS; i++) {
        if (boardState[i] >= 0)
            return false;
    }
    return true;
}
