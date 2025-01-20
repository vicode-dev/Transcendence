let score2p2d;

async function on2p_freeze(msg, gameWebSocket) {
    showNavbar();
    navBarManualOverride = false;
    if (msg.state == true) {
        loopBreaker = true;
        if (msg.players.length) {
            waitPopup();
            let ul = document.getElementById("playersList");
            let timer = document.getElementById("timer");
            let timeout = 60;

            msg.players.forEach((player) => addPlayerToList(player, ul))
            timer.innerHTML = timeout;
            while (timeout >= 0) {
                await sleep(1000);
                timeout--;
                timer.innerHTML = timeout;

            }
        }
    }
    else if (msg.state == false) {
        let modal = document.getElementById("modal")
        modal.style.display = "none";
        loopBreaker = false;
        await startAnimation();
        on2p_gameLoop(gameWebSocket);
    }
}

function on2p_UpdateGameData(data) {
    if (data.P) {
        p1 = data.P[0];
        p2 = data.P[1];
    }
    ball = data.Ball;
}

function on2p_UpdateScore(data) {
    let score1 = document.getElementById("score1");
    let score2 = document.getElementById("score2");
    ball.angle = data.angle;
    score2p2d = data.scores;
    score1.textContent = data.scores[0];
    score2.textContent = data.scores[1];
}

function on2p_GameEnd(score, winner) {
    showNavbar();
    navBarManualOverride = false;
    loopBreaker = true;
    if (score == 10)
        endPopup("typeVictory", winner);
    else
        endPopup("typeDefeat", winner);
    let url = window.location.pathname.split("/");
    if (url.length > 4) {
        sleep(3000).then(function () {
            loadPage(`/tournament/${url[2]}/dashboard/`).then();
        })
    }
}

function on2p_ballReachObstacle(ball, x, y) {
    if (willHitLeftPaddle(ball, p1.x, p1.y, x, y) == true) {
        ballHitPlayer(ball, 280, 160, y - p1.y);
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (willHitRightPaddle(ball, p2.x, p2.y, x, y) == true) {
        ballHitPlayer(ball, 260, -160, y - p2.y)
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (willHitWall(x) == true) {
        if (ball.x < SIZE / 2)
            ball.x = BALL_SIZE;
        else
            ball.x = SIZE - BALL_SIZE;
    }
    else if (willHitWall(y) == true) {
        if (ball.y < SIZE / 2)
            ball.y = BALL_SIZE;
        else
            ball.y = SIZE - BALL_SIZE;
        if (ball.angle % 90 === 0)
            ball.angle = (ball.angle + 180) % 360;
        else
            ball.angle = 360 - ball.angle;
    }
    else
        return false;
    return true;
}

function on2p_ballMovement(ball) {
    if (hitWall(ball.x)) {
        ball.angle = (ball.x - BALL_SIZE <= 0) ? 0 : 180;
        ball.x = 4.5;
        ball.y = 4.5;
        ball.speed = INIT_SPEED;
        return;
    }
    let x = ball.x + Math.cos((Math.PI / 180) * ball.angle) / 8 * ball.speed;
    let y = ball.y + Math.sin((Math.PI / 180) * ball.angle) / 8 * ball.speed;

    if (on2p_ballReachObstacle(ball, x, y) == true)
        return;
    ball.x = x;
    ball.y = y;

}

function on2p_drawPaddle() {
    let leftPaddle = document.getElementById("leftPaddle");
    let rightPaddle = document.getElementById("rightPaddle");
    leftPaddle.setAttribute("y", p1.y);
    rightPaddle.setAttribute("y", p2.y);
}

// function setNavbarInactivityTimeout(secAmount) {
//     clearTimeout(inactivityTimeout);
//     inactivityTimeout = setTimeout(() => {
//       document.getElementById("nav").style.bottom = "0";
//     }, secAmount);
// }



async function on2p_gameLoop(gameWebSocket) {
    hideNavbar();
    clearTimeout(inactivityTimeout);
    while (1) {
        const startTime = Date.now();
        on2p_ballMovement(ball)
        drawBall(ball)
        on2p_drawPaddle()
        sendMove(gameWebSocket)
        const EndTime = Date.now();
        let elapsedTime = startTime - EndTime;
        await sleep(Math.max(0, TICK_RATE - (elapsedTime / 1000)) * 1000)
        if (loopBreaker === true)
            break;
    }
    loopBreaker = false;
    navBarManualOverride = false;
}

function on2p_init(playersList) {
    let players = ["player1", "player2"];

    for (let i = 0; i < players.length; i++) {
        let name = document.getElementById(players[i]);
        name.src = "/api/player/" + playersList[i] + "/avatar/";
    }
}

function on2p_keydownEvent(event) {
    if (event.key === "ArrowLeft") {
        paddleMove = -1;
    } else if (event.key === "ArrowRight") {
        paddleMove = 1;
    }    
}

function on2p_closeEvent() {
    let SVGBall = document.getElementById("ball");
    SVGBall.style.display = "none";
    loopBreak = true;
    if (error == true) {
        crashPopup();
    }
}

function on2p_openEvent() {
    gameWebSocket.send(JSON.stringify({'type':'refresh'}));
}

function on2p_messageEvent(event) {
    let msg = JSON.parse(event.data)
    switch (msg.type) {
        case "init":
            on2p_init(msg['playersList']);
            break;
        case "tick_data":
            on2p_UpdateGameData(msg);
            if (state == false)
            {
                drawBall();
                on2p_drawPaddle();
            }
            break;
        case "score_update":
            on2p_UpdateScore(msg);
            break;
        case "game_end":
            on2p_GameEnd(msg['score'], msg['winner']);
            error = false;
            break;
        case "freeze":
            state = msg.state;
            on2p_freeze(msg, gameWebSocket);
    }

}

function mainGameLoop2pOnline() {
    state = false;
    gameWebSocket = new WebSocket(`wss://${window.location.host}/ws/game/${document.querySelector('[name=gameId]').value}/2pong`);
    ball = new Ball(4.5, 4.5, 195);
    p1 = new Player(0, 3.75);
    p2 = new Player(8.75, 3.75);
    score2p2d = [0, 0]
    paddleMove = 0;
    loopBreaker = false;
    error = true;
    destructors.push(on2p_destructor);
    gameWebSocket.addEventListener("message", on2p_messageEvent);
    gameWebSocket.addEventListener("close", on2p_closeEvent);
    document.addEventListener("keydown", on2p_keydownEvent);
    gameWebSocket.addEventListener('open', on2p_openEvent);
    window.addEventListener("resize", resizeHandler);
}

function on2p_destructor() {
    p1 = null;
    p2 = null;
    ball = null;
    document.removeEventListener("keydown", on2p_keydownEvent);
    gameWebSocket.removeEventListener("close", on2p_closeEvent);
    gameWebSocket.removeEventListener('open', on2p_openEvent);
    gameWebSocket.removeEventListener("message", on2p_messageEvent);
    enableDoubleTapZoom();
    window.removeEventListener("resize", resizeHandler);
    gameWebSocket.close();
}

addMain(mainGameLoop2pOnline);

