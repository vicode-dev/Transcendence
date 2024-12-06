class Ball {

    constructor(x, y, angle) {
        this.x = x;
        this.y = y;
        this.angle = 180;
        this.speed = 1;
    }
}

class Player {

    constructor(x, y) {
        this.y = y;
        this.x = x;

    }
}

const SIZE = 9;
const PADDLE_SIZE = 1.5;
const PADDLE_WIDTH = 0.25;
const BALL_SIZE = 0.125;
const TICK_RATE = 1/20;
const MAX_SPEED = 10;
let p1 = new Player(0, 3.75);
let p2 = new Player(8.75, 3.75);

document.addEventListener("keydown", (event) => {
    let leftPaddle = document.getElementById("leftPaddle");
    if (!leftPaddle)
        return ;
    if (event.key === "ArrowUp" && p1.y > 0) {
        p1.y -= 0.25;
    } else if (event.key === "ArrowDown" && p1.y < SIZE - PADDLE_SIZE) {
        p1.y += 0.25;
    }
    leftPaddle.setAttribute("y", p1.y);
});

document.addEventListener("keydown", (event) => {
    let rightPaddle = document.getElementById("rightPaddle");
    if (!rightPaddle)
        return ;
    if (event.key === "ArrowLeft" && p2.y > 0) {
        p2.y -= 0.25;
    } else if (event.key === "ArrowRight" && p2.y < SIZE - PADDLE_SIZE) {
        p2.y += 0.25;
    }
    rightPaddle.setAttribute("y", p2.y);
});

function willHitLeftPaddle(ball, px, py, x, y) {
    if ((x - BALL_SIZE < px + PADDLE_WIDTH && py <= y - BALL_SIZE && y - BALL_SIZE <= py + PADDLE_SIZE))
        ball.x = px + PADDLE_WIDTH + BALL_SIZE;
    else if (x - BALL_SIZE < px + PADDLE_WIDTH && py <= y + BALL_SIZE && y + BALL_SIZE <= py + PADDLE_SIZE)
        ball.x = px + PADDLE_WIDTH + BALL_SIZE;
    else
        return false;
    return true;
}

function willHitRightPaddle(ball, px, py, x, y) {
    if ((px < x + BALL_SIZE && py <= y + BALL_SIZE && y + BALL_SIZE <= py + PADDLE_SIZE))
        ball.x = px - BALL_SIZE;
    else if ((px < x + BALL_SIZE && py <= y - BALL_SIZE && y - BALL_SIZE <= py + PADDLE_SIZE))
        ball.x = px - BALL_SIZE;
    else
        return false;
    return true;
}

function hitWall(x) {
    if (x - BALL_SIZE == 0 || x + BALL_SIZE == SIZE)
        return true
    return false
}

function willHitWall(x) {
    if (x - BALL_SIZE < 0 || x + BALL_SIZE > SIZE)
        return true
    return false
}

function ballHitPlayer(ball, startAngle, diff, ballPos) {
    ball.angle = (360 + startAngle + (diff / (PADDLE_SIZE + 2 * BALL_SIZE)) * (ballPos + BALL_SIZE)) % 360
}

function ballReachObstacle(ball, x, y) {
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

function ballMovement(ball, scores) {
    if (hitWall(ball.x)) {
        if (ball.x - BALL_SIZE <= 0) {
            ball.angle = 0;
            scores[1] += 1;
        }
        else {
            ball.angle = 180;
            scores[0] += 1;
        }
        UpdateScore(scores);
        ball.angle = (ball.x - BALL_SIZE <= 0) ? 0 : 180;
        ball.x = 4.5;
        ball.y = 4.5;
        ball.speed = 1;
    }
    let x = ball.x + Math.cos((Math.PI / 180) * ball.angle) / 8 * ball.speed;
    let y = ball.y + Math.sin((Math.PI / 180) * ball.angle) / 8 * ball.speed;

    if (ballReachObstacle(ball, x, y) == true)
        return;
    ball.x = x;
    ball.y = y;
}

function UpdateScore(scores) {
    score1 = document.getElementById("score1");
    score2 = document.getElementById("score2");
    score1.textContent = scores[0];
    score2.textContent = scores[1];
}

// document.addEventListener('DOMContentLoaded', gameLoop, false);
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function drawBall(ball) {
    let SVGBall = document.getElementById("ball");
    SVGBall.style.transition = '';
    SVGBall.style.transform = `translate(${ball.x}px, ${ball.y}px)`;
}

async function gameLoop() {
    ball = new Ball(4.5, 4.5);
    scores = [0, 0];
    while(scores[0] < 10 && scores[1] < 10) {
        const startTime = Date.now();
        ballMovement(ball, scores);
        drawBall(ball);
        const EndTime = Date.now();
        elapsedTime = startTime - EndTime;
        await sleep(Math.max(0, TICK_RATE - (elapsedTime / 1000)) * 1000)
    }
    GameEnd(scores);
}