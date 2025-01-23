function of2p_ballReachObstacle(ball, x, y) {
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

function of2p_ballMovement(ball, scores) {
    if (hitWall(ball.x)) {
        if (ball.x - BALL_SIZE <= 0) {
            ball.angle = 0 + randomAngle();
            scores[1] += 1;
        }
        else {
            ball.angle = 180 + randomAngle();
            scores[0] += 1;
        }
        of2p_UpdateScore(scores);
        ball.x = 4.5;
        ball.y = 4.5;
        ball.speed = INIT_SPEED;
        return;
    }
    let x = ball.x + Math.cos((Math.PI / 180) * ball.angle) / 8 * ball.speed;
    let y = ball.y + Math.sin((Math.PI / 180) * ball.angle) / 8 * ball.speed;

    if (of2p_ballReachObstacle(ball, x, y) == true)
        return;
    ball.x = x;
    ball.y = y;
}

function of2p_UpdateScore(scores) {
    let score1 = document.getElementById("score1");
    let score2 = document.getElementById("score2");
    score1.textContent = scores[0];
    score2.textContent = scores[1];
}

function of2p_GameEnd(scores) {
    let box = document.getElementById("winner-msg");
    let winner;
    
    winner = scores[0] == 10 ? 1 : 2;
    box.innerHTML = winner;
    document.getElementById("winner-msg-content").style.visibility = "visible";
    exitFullScreen();
}


function blockContextMenu() {
    window.oncontextmenu = function(event) {
        if (event.button !== 2) {
            event.preventDefault();
        }
    };
}

async function of2p_gameLoop() {
    disableDoubleTapZoom();
    enterFullScreen();
    listenForScreenChange();
    blockContextMenu();
    
    let scores = [0, 0];
    document.getElementById("start-btn").style.visibility = "hidden";
    document.getElementById("winner-msg-content").style.visibility = "hidden";
    ball = new Ball(4.5, 4.5, 195);
    p1 = new Player(0, 3.75);
    p2 = new Player(8.75, 3.75);
    initPos();
    window.addEventListener("resize", resizeHandler);
    destructors.push(of2p_destructor);
    while(scores[0] < 10 && scores[1] < 10) {
        const startTime = Date.now();
        of2p_ballMovement(ball, scores);
        drawBall(ball);
        const EndTime = Date.now();
        let elapsedTime = startTime - EndTime;
        await sleep(Math.max(0, TICK_RATE - (elapsedTime / 1000)) * 1000)
        if (ball == null || p1 == null || p2 == null)
            break;
    }
    document.getElementById("start-btn").style.visibility = "visible";
    of2p_GameEnd(scores);
}

function of2p_move(event) {
    if (event.key === "w" || event.key === "s") {
        moveLeftPaddle(event.key);
    }
    else if (event.key === "ArrowUp" || event.key === "ArrowDown") {
        moveRightPaddle(event.key);
    }
}

function mainPong2pOffline() {
    // Disable pinch zoom
    document.addEventListener('gesturestart', preventDefaultHandler);
    document.addEventListener('gesturechange', preventDefaultHandler);
    document.addEventListener('gestureend', preventDefaultHandler);

    document.addEventListener("keydown", of2p_move);
    document.getElementById("winner-msg-content").style.visibility = "hidden";
}

function of2p_destructor() {
    p1 = null;
    p2 = null;
    ball = null;
    document.removeEventListener("keydown", of2p_move);

    document.removeEventListener('gesturestart', preventDefaultHandler);
    document.removeEventListener('gesturechange', preventDefaultHandler);
    document.removeEventListener('gestureend', preventDefaultHandler);
    window.removeEventListener("resize", resizeHandler);

    unblockContextMenu();
    enableDoubleTapZoom();
}

addMain(mainPong2pOffline);