let scores2d;

async function on4p_freeze(msg) {
    showNavbar();
    navBarManualOverride = false;
    let state = msg.state;
    if (msg.state == true) {
        loopBreaker = true;
        if (msg.players.length) {
            waitPopup();
            let timer = document.getElementById("timer");
            let timeout = 60;
            let ul = document.getElementById("playersList");

            msg.players.forEach((player) => addPlayerToList(player, ul))
            timer.innerHTML = timeout;
            while (state && timeout >= 0) 
            {
                await sleep(1000);
                timeout--;
                timer.innerHTML = timeout;
            
            }
        }
    }
    else if (msg.state == false)
    {
        let modal = document.getElementById("modal")
        modal.style.display = "none";
        loopBreaker = false;
        await startAnimation();
        on4p_gameLoop(gameWebSocket);  
    }
}

function on4p_UpdateGameData(data) {
    p1 = data.P[0];
    p2 = data.P[1];
    p3 = data.P[2];
    p4 = data.P[3];
    ball = data.Ball;
}

function on4p_UpdateScore(score) {
    let score1 = document.getElementById("score3");
    let score2 = document.getElementById("score4");
    let score3 = document.getElementById("score2");
    let score4 = document.getElementById("score1");
    ball.angle = score.angle;
    if (score[0] >= 0)
        score1.textContent = score[0];
    if (score[1] >= 0)
        score2.textContent = score[1];
    if (score[2] >= 0)
        score3.textContent = score[2];
    if (score[3] >= 0)
        score4.textContent = score[3];
}

function on4p_GameEnd(score, winner) {
    showNavbar();
    navBarManualOverride = false;
    loopBreaker = true;
    console.log("winner, score", winner, score);
    if (on_index == null)
        endPopup("typeVictory", winner);
    else if (score[on_index] == 1)
        endPopup("typeVictory", winner);
    else
        endPopup("typeDefeat", winner);
    showNavbar();
}

function on4p_ballReachObstacle(ball, x, y) {
    if (scores2d[0] > 0 && willHitLeftPaddle(ball, p1.x, p1.y, x, y) == true) {
        ballHitPlayer(ball, 280, 160, y - p1.y);
        ball.speed += 0.1;
    }
    else if (scores2d[1] > 0 && willHitRightPaddle(ball, p2.x, p2.y, x, y) == true) {
        ballHitPlayer(ball, 260, -160, y - p2.y)
        ball.speed += 0.1;
    }
    else if (scores2d[2] > 0 && willHitTopPaddle(ball, p3.x, p3.y, x, y) == true) {
        ballHitPlayer(ball, 170, -160, x - p3.x)
        ball.speed += 0.1;
    }
    else if (scores2d[3] > 0 && willHitBottomPaddle(ball, p4.x, p4.y, x, y) == true) {
        ballHitPlayer(ball, 190, 160, x - p4.x)
        ball.speed += 0.1;
    }
    else if (willHitWall(x) == true) {
        if (ball.x < SIZE / 2) {
            ball.x = BALL_SIZE;
            if (scores2d[0] <= 0) {
                if (ball.angle % 90 == 0)
                    ball.angle = 180 + ball.angle;
                else
                    ball.angle = (360 + 180 - ball.angle) % 360;
            }
        }
        else {
            ball.x = SIZE - BALL_SIZE;
            if (scores2d[1] <= 0) {
                if (ball.angle % 90 == 0)
                    ball.angle = 180 + ball.angle;
                else
                    ball.angle = (360 + 180 - ball.angle) % 360;
            }
        }
    }
    else if (willHitWall(y) == true) {
        if (ball.y < SIZE / 2) {
            ball.y = BALL_SIZE;
            if (scores2d[2] <= 0) {
                if (ball.angle % 180 == 0)
                    ball.angle = (ball.angle + 180) % 360;
                else
                    ball.angle = 360 - ball.angle;
            }
        }
        else {
            ball.y = SIZE - BALL_SIZE;
            if (scores2d[3] <= 0) {
                if (ball.angle % 180 == 0)
                        ball.angle = (ball.angle + 180) % 360;
                    else
                        ball.angle = 360 - ball.angle;
            }
        }
    }
    else
        return false;
    return true;
}

function on4p_ballMovement(ball) {
    if (ball == null)
        return;
    if (hitWall(ball.x) || hitWall(ball.y))
    {
        let playersAreWall = true;
        if (hitWall(ball.x)) {
            if (scores2d[0] > 0 && ball.x - BALL_SIZE <= 0) {
                playersAreWall = false;
                // ball.angle = 0;
            }
            else if (scores2d[1] > 0 && ball.x + BALL_SIZE >= SIZE) {
                playersAreWall = false;
                // ball.angle = 180;
            }
        }
        else {
            if (scores2d[2] > 0 && ball.y - BALL_SIZE <= 0) {
                playersAreWall = false;
                // ball.angle = 90;
            }
            else if (scores2d[3] > 0 && ball.y + BALL_SIZE >= SIZE) {
                playersAreWall = false;
                // ball.angle = 270;
            }
        }
        if (playersAreWall == false) {
            ball.x = 4.5;
            ball.y = 4.5;
            ball.speed = INIT_SPEED;
            return;
        }
    }
    let x = ball.x + Math.cos((Math.PI / 180) * ball.angle) / 8 * ball.speed;
    let y = ball.y + Math.sin((Math.PI / 180) * ball.angle) / 8 * ball.speed;

    if (on4p_ballReachObstacle(ball, x, y) == true)
        return;
    ball.x = x;
    ball.y = y;
    
}

function on4p_drawPaddle() {
    let leftPaddle = document.getElementById("leftPaddle");
    let rightPaddle = document.getElementById("rightPaddle");
    let topPaddle = document.getElementById("topPaddle");
    let bottomPaddle = document.getElementById("bottomPaddle");
    if (leftPaddle == null || rightPaddle == null || topPaddle == null || bottomPaddle == null)
        return;
    let idxBoard = [0, 1, 2, 3]
    if (scores2d[idxBoard[0]] > 0)
        leftPaddle.setAttribute("y", p1.y);
    else
        leftPaddle.style.display = 'none';
    if (scores2d[idxBoard[1]] > 0)
        rightPaddle.setAttribute("y", p2.y);
    else
        rightPaddle.style.display = 'none';
    if (scores2d[idxBoard[2]] > 0)
        topPaddle.setAttribute("x", p3.x);
    else
        topPaddle.style.display = 'none';
    if (scores2d[idxBoard[3]] > 0)
        bottomPaddle.setAttribute("x", p4.x);
    else
        bottomPaddle.style.display = 'none';
}

async function on4p_gameLoop(gameWebSocket) {
    hideNavbar();
    clearTimeout(inactivityTimeout);
    while(1) {
        const startTime = Date.now();
        on4p_ballMovement(ball);
        drawBall(ball)
        on4p_drawPaddle();
        sendMove(gameWebSocket);
        const EndTime = Date.now();
        let elapsedTime = startTime - EndTime;
        await sleep(Math.max(0, TICK_RATE - (elapsedTime / 1000)) * 1000)
        if (loopBreaker === true)
            break;
    }
    loopBreaker = false;
    navBarManualOverride = false;
}

function on4p_keydownEvent(event) {
    if (on_index == 1 || on_index == 2)
        move = -1;
    else
        move = 1;
    if (event.key == "ArrowLeft") 
        paddleMove = -move;
    else if (event.key == "ArrowRight")
        paddleMove = move;
}

function on4p_init(msg) {
    let playersList = msg["playersList"];
    let players = ["player1", "player2", "player3", "player4"];
    let name;

    for (let i = 0; i < players.length; i++) {
        name = document.getElementById(players[i]);
        if (name == null)
            continue;
        fetch("/api/player/" + playersList[i] + "/username/")
        .then(data => {
            return data.text();
        })
        .then(user => {
            let username = JSON.parse(user);
            name.innerHTML = username.username;
        })
    }
}

function on4p_closeEvent() {
    loopBreaker = true;
    if (error == true) {
        crashPopup();
    }
}

function on4p_openEvent() {
    gameWebSocket.send(JSON.stringify({'type':'refresh'}));
    gameWebSocket.send(JSON.stringify({'type':'index'}));
}

function on4p_messageEvent(event) {
    let msg = JSON.parse(event.data)
    switch (msg.type) {
        case "init":
            on4p_init(msg);
            break;
        case "tick_data":
            on4p_UpdateGameData(msg);
            if (state == false)
                {
                    drawBall();
                    on4p_drawPaddle();
                }
            break;
        case "score_update":
            scores2d[0] = msg.scores[0];
            scores2d[1] = msg.scores[1];
            scores2d[2] = msg.scores[2];
            scores2d[3] = msg.scores[3];
            if(on_index != null)
            {
                let diff;
                let keep = [msg.scores[0], msg.scores[2], msg.scores[1], msg.scores[3]];
                if (on_index == 0 || on_index == 3)
                    diff = 3 - on_index;
                else
                    diff = on_index;
                for (let i = 0; i < 4; i++) {
                    msg.scores[(i + diff) % 4] = keep[i];
                }
                let save = msg.scores[1]
                msg.scores[1] = msg.scores[2];
                msg.scores[2] = save;
            }
            on4p_UpdateScore(msg.scores);
            break;
        case "game_end":
            on4p_GameEnd(msg.score, msg.winner);
            error = false;
            break;
        case "freeze":
            state = msg.state;
            on4p_freeze(msg, gameWebSocket);
            break;
        case "index":
            on_index = msg.index;
            on_rotate(on_index);
            console.log("Index is " + on_index);
            break;
    }
}

function mainGameLoop4pOnline()
{
    state = false;
    gameWebSocket = new WebSocket(
        'wss://'
        + window.location.host
        + '/ws/game/'
        + document.querySelector('[name=gameId]').value
        + '/4pong'
    );
    ball = new Ball(4.5, 4.5, 195);
    p1 = new Player(0, 3.75);
    p2 = new Player(8.75, 3.75);
    p3 = new Player(3.75, 0);
    p4 = new Player(3.75, 8.75);
    scores2d = [5, 5, 5, 5];
    paddleMove = 0;
    loopBreaker = false;
    error = true;
    destructors.push(on4p_destructor);
    gameWebSocket.addEventListener("message", on4p_messageEvent);
    gameWebSocket.addEventListener("close", on4p_closeEvent);
    gameWebSocket.addEventListener('open', on4p_openEvent);
    document.addEventListener("keydown", on4p_keydownEvent);
}

function on4p_destructor() {
    gameWebSocket.close();
    p1 = null;
    p2 = null;
    p3 = null;
    p4 = null;
    ball = null;
    scores2d = null;
    gameWebSocket.removeEventListener("close", on4p_closeEvent);
    gameWebSocket.removeEventListener('open', on4p_openEvent);
    gameWebSocket.removeEventListener("message", on4p_messageEvent);
    document.removeEventListener("keydown", on4p_keydownEvent);
    unblockContextMenu();
    enableDoubleTapZoom();
}

addMain(mainGameLoop4pOnline);