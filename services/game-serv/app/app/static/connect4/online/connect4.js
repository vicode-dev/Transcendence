let freezeState;
let connectWebSocket;


// document.addEventListener('DOMContentLoaded', function () {


function onc_UpdateGameData(msg) {
    boardState = msg["board_state"];
    turn = msg["turn"];
}

function onc_freeze(msg, connectWebSocket) {
    freezeState = msg["state"];
}

function onc_dropPiece(connectWebSocket, col) {
    if (freezeState == false)
        connectWebSocket.send(JSON.stringify({"type": "move", "dropPiece": col}));
}

function onc_drawPiece(col) {
    let color = [backgroundColor, accentColor];

    if (boardState[col] + 1 >= 0) {
        board[boardState[col] + 1][col] = turn;
        let svg = document.getElementById("pieces");
        let piece = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        piece.setAttribute("r", 20);
        piece.setAttribute("fill", color[(turn + 1) % 2]);
        piece.setAttribute("cx", 25 + 50 * col);
        piece.setAttribute("cy", 25 + (boardState[col] + 1) * 50);
        piece.setAttribute("class", "Piece");
        if (turn % 2 === 1) {
            piece.setAttribute("stroke", accentColor);
            piece.setAttribute("stroke-width", "5");
        }
        svg.appendChild(piece);
        onc_updatePlayersBtnColor();
    }
}

function onc_updatePlayersBtnColor() {
    if (turn % 2 == 0) {
        playerBtn1.style.backgroundColor = accentColor;
        playerBtn2.style.backgroundColor = "";
    } else {
        playerBtn2.style.backgroundColor = accentColor;
        playerBtn1.style.backgroundColor = "";
    }
}

function onc_players(players) {
    let playersFront = ["player1", "player2"];

    for (let i = 0; i < 2; i++) {
        let player = document.getElementById(playersFront[i]);
        fetch ("/api/player/" + players[i] + "/username/")
            .then(data => {
                return data.text();
            })
            .then(user => {
                let username = JSON.parse(user);
                player.innerHTML = username.username;
            })
    }
}

function onc_redraw(players) {
    let color = [backgroundColor, accentColor];
    onc_players(players);
    for (let i = 0; i < COLUMNS; i++) {
        for (let j = boardState[i] + 1; j < ROWS; j++) {
            let svg = document.getElementById("pieces");
            let piece = document.createElementNS("http://www.w3.org/2000/svg", "circle");
            piece.setAttribute("r", 20);
            piece.setAttribute("fill", color[board[j][i] - 1]);
            piece.setAttribute("cx", 25 + 50 * i);
            piece.setAttribute("cy", 25 + (j) * 50);
            piece.setAttribute("class", "Piece");
            if (board[j][i] % 2 === 1) {
                piece.setAttribute("stroke", accentColor);
                piece.setAttribute("stroke-width", "5");
            }
            svg.appendChild(piece);
        }
    }
}

function onc_endGame(msg) {
    let score = msg["score"];
    let winFront = document.getElementById("end_msg");
    freezeState = true;
    if (score[0] == 0 && score[1] == 0) {
        document.getElementById("draw-msg").style.visibility = "visible";
    }
    else {
        document.getElementById("win-msg").style.visibility = "visible";
    }
    fetch ("/api/player/" + msg["winner"] + "/username/")
        .then(data => {
            return data.text();
        })
        .then(user => {
            let username = JSON.parse(user);
            winFront.innerHTML = username.username;
        })
}

function onc_messageEvent(event) {
    let msg = JSON.parse(event.data)
    switch (msg.type) {
        case "data":
            onc_UpdateGameData(msg);
            onc_drawPiece(msg["col"]);
            break;
        case "error":
            console.log(msg);
            break;
        case "start_game":
            onc_players(msg['players']);
            break;
        case "end_game":
            onc_endGame(msg);
            break;
        case "freeze":
            onc_freeze(msg, connectWebSocket);
            break;
        case "board":
            board = msg["board"];
            boardState = msg["board_state"];
            onc_redraw(msg["players"]);
            break;
    }
}

function onc_openEvent() {
    connectWebSocket.send(JSON.stringify({"type": "reconnect"}));
}

function onc_c1Drop() {
    onc_dropPiece(connectWebSocket, 0);
}

function onc_c2Drop() {
    onc_dropPiece(connectWebSocket, 1);
}

function onc_c3Drop() {
    onc_dropPiece(connectWebSocket, 2);
}

function onc_c4Drop() {
    onc_dropPiece(connectWebSocket, 3);
}

function onc_c5Drop() {
    onc_dropPiece(connectWebSocket, 4);
}

function onc_c6Drop() {
    onc_dropPiece(connectWebSocket, 5);
}

function onc_c7Drop() {
    onc_dropPiece(connectWebSocket, 6);
}

function mainConnectOnline() {
    let c1 = document.getElementById("c1");
    let c2 = document.getElementById("c2");
    let c3 = document.getElementById("c3");
    let c4 = document.getElementById("c4");
    let c5 = document.getElementById("c5");
    let c6 = document.getElementById("c6");
    let c7 = document.getElementById("c7");

    connectWebSocket = new WebSocket(
        'wss://'
        + window.location.host
        + '/ws/game/'
        + document.querySelector('[name=gameId]').value
        + '/connect4'
    );
    board = new Array(ROWS);
    freezeState = false
    for (let i = 0; i < ROWS; i++) {
        board[i] = new Array(COLUMNS).fill(0);
    }
    boardState = new Array(COLUMNS).fill(ROWS - 1);
    turn = 0;
    gameOver = 0;
    playerBtn1 = document.getElementById("player-btn-1");
    playerBtn2 = document.getElementById("player-btn-2");
    document.getElementById("start-again").style.visibility = "hidden";
    document.getElementById("win-msg").style.visibility = "hidden";
    document.getElementById("draw-msg").style.visibility = "hidden";
    destructors.push(onc_destructor);
    connectWebSocket.addEventListener("message", onc_messageEvent);
    connectWebSocket.addEventListener("open", onc_openEvent);
    c1.addEventListener('click', onc_c1Drop);
    c2.addEventListener('click', onc_c2Drop);
    c3.addEventListener('click', onc_c3Drop);
    c4.addEventListener('click', onc_c4Drop);
    c5.addEventListener('click', onc_c5Drop);
    c6.addEventListener('click', onc_c6Drop);
    c7.addEventListener('click', onc_c7Drop);
}

function onc_destructor() {
    boardState = 0;
    board = 0;
    connectWebSocket.removeEventListener("message", onc_messageEvent);
    connectWebSocket.removeEventListener("open", onc_openEvent);
    c1.removeEventListener('click', onc_c1Drop);
    c2.removeEventListener('click', onc_c2Drop);
    c3.removeEventListener('click', onc_c3Drop);
    c4.removeEventListener('click', onc_c4Drop);
    c5.removeEventListener('click', onc_c5Drop);
    c6.removeEventListener('click', onc_c6Drop);
    c7.removeEventListener('click', onc_c7Drop);
    connectWebSocket.close();
}

addMain(mainConnectOnline);
