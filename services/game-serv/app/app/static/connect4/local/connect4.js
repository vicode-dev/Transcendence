let gameOver;
let playerBtn1;
let playerBtn2;

let player1Score;
let player2Score;


// document.addEventListener('DOMContentLoaded', function () {

function ofc_dropPiece(col) {
    if (boardState[col] >= 0 && gameOver == 0) {
        board[boardState[col]][col] = turn + 1;
        if (checkWin(boardState[col], col) == true) {
            gameOver = 2;
            ofc_finishGameUpdate();
        }
        let svg = document.getElementById("pieces");
        let piece = document.createElementNS("http://www.w3.org/2000/svg", "circle");

        piece.setAttribute("r", 20);
        piece.setAttribute("fill", COLOR[turn]);
        piece.setAttribute("cx", 25 + 50 * col);
        piece.setAttribute("cy", 25 + boardState[col] * 50);
        piece.setAttribute("class", "Piece");
        if (turn % 2 === 0) {
            piece.setAttribute("stroke", accentColor);
            piece.setAttribute("stroke-width", "5");
        }
        svg.appendChild(piece);
        boardState[col] -= 1;
        turn = (turn + 1) % 2;
        
        ofc_updatePlayersBtnColor();
        if (boardFull() == true) {
            gameOver = 1;

            let msg = document.getElementById('end_msg');
            msg.innerHTML = "<p>Game has two losers :(</p>";
        }
    }
}

function ofc_updatePlayersBtnColor() {
    if (turn % 2 == 0) {
        playerBtn1.style.backgroundColor = accentColor;
        playerBtn2.style.backgroundColor = "";
    } else {
        playerBtn2.style.backgroundColor = accentColor;
        playerBtn1.style.backgroundColor = ""; 
    }
}

function ofc_finishGameUpdate() {
    let msg = document.getElementById('end_msg');

    // startBtn = document.getElementById("start-again").style.display = "block";

    if (turn % 2 == 0)
    {
        msg.innerHTML = "<p>Player 1 won!</p>";
        document.getElementById("player1-score").remove();
        
        let newScore = document.createElement("div");
        newScore.setAttribute("id", "player1-score");
        newScore.innerHTML = (player1Score += 1);
        playerBtn1.append(newScore);
    }
    else
    {
        msg.innerHTML = "<p>Player 2 won!</p>";
        document.getElementById("player2-score").remove();
        
        let newScore = document.createElement("div");
        newScore.setAttribute("id", "player2-score");
        newScore.innerHTML = (player2Score += 1);
        playerBtn2.append(newScore);
    }
    document.getElementById("start-again").style.visibility = "visible";
}

function ofc_newGame() {
    document.getElementById("pieces").replaceChildren();
    document.getElementById('end_msg').innerHTML = '';
    document.getElementById("start-again").style.visibility = "hidden";
    for (let i = 0; i < boardState.length; i++)
        boardState[i] = ROWS - 1;
    for (let i = 0; i < board.length; i++) {
        for (let j = 0; j < board[i].length; j++)
            board[i][j] = 0;
    }
    turn = 0;
    gameOver = 0;
}

function ofc_c1Drop() {
    ofc_dropPiece(0);
}

function ofc_c2Drop() {
    ofc_dropPiece(1);
}

function ofc_c3Drop() {
    ofc_dropPiece(2);
}

function ofc_c4Drop() {
    ofc_dropPiece(3);
}

function ofc_c5Drop() {
    ofc_dropPiece(4);
}

function ofc_c6Drop() {
    ofc_dropPiece(5);
}

function ofc_c7Drop() {
    ofc_dropPiece(6);
}

function mainConnectOffline() {
    board = new Array(ROWS);
    for (let i = 0; i < ROWS; i++) {
        board[i] = new Array(COLUMNS).fill(0);
    }
    boardState = new Array(COLUMNS).fill(ROWS - 1);
    turn = 0;
    gameOver = 0;
    playerBtn1 = document.getElementById("player-btn-1");
    playerBtn2 = document.getElementById("player-btn-2");
    player1Score = 0;
    player2Score = 0;
    destructors.push(ofc_destructor);
    // document.getElementById("start-again").style.display = "none";
    document.getElementById("start-again").style.visibility = "hidden";
    document.getElementById("player1-score").innerHTML = 0;
    document.getElementById("player2-score").innerHTML = 0;
    playerBtn1.style.backgroundColor = accentColor;

    c1.addEventListener('click', ofc_c1Drop);
    c2.addEventListener('click', ofc_c2Drop);
    c3.addEventListener('click', ofc_c3Drop);
    c4.addEventListener('click', ofc_c4Drop);
    c5.addEventListener('click', ofc_c5Drop);
    c6.addEventListener('click', ofc_c6Drop);
    c7.addEventListener('click', ofc_c7Drop);
}

function ofc_destructor() {
    boardState = 0;
    board = 0;
    c1.removeEventListener('click', ofc_c1Drop);
    c2.removeEventListener('click', ofc_c2Drop);
    c3.removeEventListener('click', ofc_c3Drop);
    c4.removeEventListener('click', ofc_c4Drop);
    c5.removeEventListener('click', ofc_c5Drop);
    c6.removeEventListener('click', ofc_c6Drop);
    c7.removeEventListener('click', ofc_c7Drop);
}

addMain(mainConnectOffline);