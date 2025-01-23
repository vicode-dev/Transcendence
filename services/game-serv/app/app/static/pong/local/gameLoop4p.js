function of4p_UpdateScore(score) {
    let score1 = document.getElementById("score1");
    let score2 = document.getElementById("score2");
    let score3 = document.getElementById("score3");
    let score4 = document.getElementById("score4");
    if (score[0] >= 0)
        score1.textContent = score[0];
    if (score[1] >= 0)
        score2.textContent = score[1];
    if (score[2] >= 0)
        score3.textContent = score[2];
    if (score[3] >= 0)
        score4.textContent = score[3];
}

function of4p_ballReachObstacle(ball, scores, x, y) {
    if (scores[0] > 0 && willHitLeftPaddle(ball, p1.x, p1.y, x, y) == true) {
        ballHitPlayer(ball, 280, 160, y - p1.y);
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (scores[1] > 0 && willHitRightPaddle(ball, p2.x, p2.y, x, y) == true) {
        ballHitPlayer(ball, 260, -160, y - p2.y)
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (scores[2] > 0 && willHitTopPaddle(ball, p3.x, p3.y, x, y) == true) {
        ballHitPlayer(ball, 170, -160, x - p3.x)
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (scores[3] > 0 && willHitBottomPaddle(ball, p4.x, p4.y, x, y) == true) {
        ballHitPlayer(ball, 190, 160, x - p4.x)
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (willHitWall(x) == true) {
        if (ball.x < SIZE / 2) {
            ball.x = BALL_SIZE;
            if (scores[0] <= 0) {
                if (ball.angle % 90 == 0)
                ball.angle = 180 + ball.angle;
                else
                    ball.angle = (360 + 180 - ball.angle) % 360;
                }
            }
            else {
                ball.x = SIZE - BALL_SIZE;
                if (scores[1] <= 0) {
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
            if (scores[2] <= 0) {
                if (ball.angle % 180 == 0)
                    ball.angle = (ball.angle + 180) % 360;
                else
                    ball.angle = 360 - ball.angle;
            }
        }
        else {
            ball.y = SIZE - BALL_SIZE;
            if (ball.angle % 180 == 0)
                ball.angle = (ball.angle + 180) % 360;
            else
                ball.angle = 360 - ball.angle;
        }
    }
    else
        return false;
    return true;
}

function of4p_newPoint(scores, idx) {
    let paddles = ["leftPaddle", "rightPaddle", "topPaddle", "bottomPaddle"];
    scores[idx] -= 1
    if (scores[idx] == 0) {
        let paddle = document.getElementById(paddles[idx]);
        paddle.style.display = 'none';
    }
    for (let i = 0; i < 4; i++) {
        if (i != idx && scores[i] <= 0 && scores[idx] == 0) {
            scores[i] -= 1;
        }
    }
    of4p_UpdateScore(scores);
}

function of4p_ballMovement(ball, scores) {
    if (hitWall(ball.x) || hitWall(ball.y))
    {
        let playersAreWall = true;
        if (hitWall(ball.x)) {
            if (scores[0] > 0 && ball.x - BALL_SIZE <= 0) {
                playersAreWall = false;
                of4p_newPoint(scores, 0);
                ball.angle = resetAngle(0, scores) + randomAngle();
            }
            else if (scores[1] > 0 && ball.x + BALL_SIZE >= SIZE) {
                playersAreWall = false;
                of4p_newPoint(scores, 1);
                ball.angle = resetAngle(1, scores) + randomAngle();
            }
        }
        else {
            if (scores[2] > 0 && ball.y - BALL_SIZE <= 0) {
                playersAreWall = false;
                of4p_newPoint(scores, 2);
                ball.angle = resetAngle(2, scores) + randomAngle();
            }
            else if (scores[3] > 0 && ball.y + BALL_SIZE >= SIZE) {
                playersAreWall = false;
                of4p_newPoint(scores, 3);
                ball.angle = resetAngle(3, scores) + randomAngle();
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

    if (of4p_ballReachObstacle(ball, scores, x, y) == true)
        return;
    ball.x = x;
    ball.y = y;
    
}

function of4p_victory(scores) {
    let count = 0;
    for (let i = 0; i < scores.length; i++) {
        if (scores[i] > 0)
            count++;
        if (count > 1)
            return false;
    }
    return true;
}

function of4p_GameEnd(scores) {
    // let box = document.getElementById("winner-msg");
    // let winner;
    
    // for (let i = 0; i < scores.length; i++) {
    //     if (scores[i] > 0) {
    //         winner = i + 1;
    //         break;
    //     }
    // }
    // box.innerHTML = winner;
    // document.getElementById("winner-msg-content").style.visibility = "visible";
    exitFullScreen();
}

async function of4p_gameLoop() {
    disableDoubleTapZoom();
    enterFullScreen();
    listenForScreenChange();
    blockContextMenu();
    
    let paddles = ["leftPaddle", "rightPaddle", "topPaddle", "bottomPaddle"];
    let scores = [5, 5, 5, 5];
    document.getElementById("start-btn").style.visibility = "hidden";
    // document.getElementById("winner-msg-content").style.visibility = "hidden";
    ball = new Ball(4.5, 4.5, 195);
    p1 = new Player(0, 3.75);
    p2 = new Player(8.75, 3.75);
    p3 = new Player(3.75, 0);
    p4 = new Player(3.75, 8.75);
    initPos();
    for (let i = 0; i < paddles.length; i++) {
        let paddle = document.getElementById(paddles[i]);
        paddle.style.display = 'block';
    }
    window.addEventListener("resize", resizeHandler);
    destructors.push(of4p_destructor);
    while(1) {
        const startTime = Date.now();
        of4p_ballMovement(ball, scores);
        drawBall(ball)
        if (of4p_victory(scores) == true)
            break;
        const EndTime = Date.now();
        let elapsedTime = startTime - EndTime;
        await sleep(Math.max(0, TICK_RATE - (elapsedTime / 1000)) * 1000)
        if (ball == null || p1 == null || p2 == null || p3 == null || p4 == null)
            break;
    }
    of4p_GameEnd(scores);
    document.getElementById("start-btn").style.visibility = "visible";
}

function of4p_move(event) {
    if (event.key === "w" || event.key === "s") {
        moveLeftPaddle(event.key);
    }
    else if (event.key === "ArrowUp" || event.key === "ArrowDown") {
        moveRightPaddle(event.key);
    }
    else if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
        moveTopPaddle(event.key);
    }
    else if (event.key === "a" || event.key === "d") {
        moveBottomPaddle(event.key);
    }
}

function mainPong4pOffline() {
    document.addEventListener("keydown", of4p_move);
    // Disable pinch zoom
    document.addEventListener('gesturestart', preventDefaultHandler);
    document.addEventListener('gesturechange', preventDefaultHandler);
    document.addEventListener('gestureend', preventDefaultHandler);
    // document.getElementById("winner-msg-content").style.visibility = "hidden";
}

function of4p_destructor() {
    p1 = null;
    p2 = null;
    p3 = null;
    p4 = null;
    ball = null;
    document.removeEventListener("keydown", of4p_move);
    // Pinch Zoom
    document.removeEventListener('gesturestart', preventDefaultHandler);
    document.removeEventListener('gesturechange', preventDefaultHandler);
    document.removeEventListener('gestureend', preventDefaultHandler);
    window.removeEventListener("resize", resizeHandler);

    unblockContextMenu();
    enableDoubleTapZoom();
}

addMain(mainPong4pOffline);