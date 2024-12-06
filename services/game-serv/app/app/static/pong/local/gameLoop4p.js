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
let p3 = new Player(3.75, 0);
let p4 = new Player(3.75, 8.75);

document.addEventListener("keydown", (event) => {
    let leftPaddle = document.getElementById("leftPaddle");
    if (!leftPaddle)
        return ;
    if (event.key === "ArrowUp" && p1.y > PADDLE_WIDTH) {
        p1.y -= 0.25;
    } else if (event.key === "ArrowDown" && p1.y < SIZE - PADDLE_SIZE - PADDLE_WIDTH) {
        p1.y += 0.25;
    }
    leftPaddle.setAttribute("y", p1.y);
});

document.addEventListener("keydown", (event) => {
    let rightPaddle = document.getElementById("rightPaddle");
    if (!rightPaddle)
        return ;
    if (event.key === "w" && p2.y > PADDLE_WIDTH) {
        p2.y -= 0.25;
    } else if (event.key === "s" && p2.y < SIZE - PADDLE_SIZE - PADDLE_WIDTH) {
        p2.y += 0.25;
    }
    rightPaddle.setAttribute("y", p2.y);
});

document.addEventListener("keydown", (event) => {
    let topPaddle = document.getElementById("topPaddle");
    if (!topPaddle)
        return ;
    if (event.key === "ArrowLeft" && p3.x > PADDLE_WIDTH) {
        p3.x -= 0.25;
    } else if (event.key === "ArrowRight" && p3.x < SIZE - PADDLE_SIZE - PADDLE_WIDTH) {
        p3.x += 0.25;
    }
    topPaddle.setAttribute("x", p3.x);
});

document.addEventListener("keydown", (event) => {
    let bottomPaddle = document.getElementById("bottomPaddle");
    if (!bottomPaddle)
        return ;
    if (event.key === "a" && p4.x > PADDLE_WIDTH) {
        p4.x -= 0.25;
    } else if (event.key === "d" && p4.x < SIZE - PADDLE_SIZE - PADDLE_WIDTH) {
        p4.x += 0.25;
    }
    bottomPaddle.setAttribute("x", p4.x);
});

function UpdateScore(score) {
    console.log("Hi")
    score1 = document.getElementById("score1");
    score2 = document.getElementById("score2");
    score3 = document.getElementById("score3");
    score4 = document.getElementById("score4");
    if (score[0] >= 0)
        score1.textContent = score[0];
    if (score[1] >= 0)
        score2.textContent = score[1];
    if (score[2] >= 0)
        score3.textContent = score[2];
    if (score[3] >= 0)
        score4.textContent = score[3];
}

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

function willHitTopPaddle(ball, px, py, x, y) {
    if ((y - BALL_SIZE < py + PADDLE_WIDTH && px <= x - BALL_SIZE && x - BALL_SIZE <= px + PADDLE_SIZE))
        ball.y = py + PADDLE_WIDTH + BALL_SIZE;
    else if ((y - BALL_SIZE < py + PADDLE_WIDTH && px <= x + BALL_SIZE && x + BALL_SIZE <= px + PADDLE_SIZE))
        ball.y = py + PADDLE_WIDTH + BALL_SIZE;
    else
        return false;
    return true;
}

function willHitBottomPaddle(ball, px, py, x, y) {
    if ((py < y + BALL_SIZE && px <= x + BALL_SIZE && x + BALL_SIZE <= px + PADDLE_SIZE))
        ball.y = py - BALL_SIZE;
    else if (py < y + BALL_SIZE && px <= x - BALL_SIZE && x - BALL_SIZE <= px + PADDLE_SIZE)
        ball.y = py - BALL_SIZE;
    else
        return false
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
    ball.angle = (360 + startAngle + (diff / (PADDLE_SIZE +  2 * BALL_SIZE)) * (ballPos + BALL_SIZE)) % 360
    console.log(ball.x, ball.y, ball.speed);
}


function ballReachObstacle(ball, scores, x, y) {
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

function resetAngle(idx, score) {
    angles = [180, 0, 270, 90];
    for (i = idx; i < idx + 4; i++) {
        j = i % 4;
        if (j != idx && score[j] > 0)
            return angles[j];
    }
    return 0;
}

function newPoint(scores, idx) {
    scores[idx] -= 1
    for (i = 0; i < 4; i++) {
        console.log(scores, i)
        if (i != idx && scores[i] <= 0 && scores[idx] == 0) {
            scores[i] -= 1;
        }
    }
    UpdateScore(scores);
}

function ballMovement(ball, scores) {
    if (hitWall(ball.x) || hitWall(ball.y))
    {
        playersAreWall = true;
        if (hitWall(ball.x)) {
            if (scores[0] > 0 && ball.x - BALL_SIZE <= 0) {
                playersAreWall = false;
                newPoint(scores, 0);
                ball.angle = 0;
            }
            else if (scores[1] > 0 && ball.x + BALL_SIZE >= SIZE) {
                playersAreWall = false;
                newPoint(scores, 1);
                ball.angle = 180;
            }
        }
        else {
            if (scores[2] > 0 && ball.y - BALL_SIZE <= 0) {
                playersAreWall = false;
                newPoint(scores, 2);
                ball.angle = 90;
            }
            else if (scores[3] > 0 && ball.y + BALL_SIZE >= SIZE) {
                playersAreWall = false;
                newPoint(scores, 3);
                ball.angle = 270;
            }
        }
        if (playersAreWall == false) {
            ball.x = 4.5;
            ball.y = 4.5;
            ball.speed = 1;
        }
    }
    let x = ball.x + Math.cos((Math.PI / 180) * ball.angle) / 8 * ball.speed;
    let y = ball.y + Math.sin((Math.PI / 180) * ball.angle) / 8 * ball.speed;

    if (ballReachObstacle(ball, scores, x, y) == true)
        return;
    ball.x = x;
    ball.y = y;
    
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
    ball = new Ball(4.25, 4.25);
    scores = [5, 5, 5, 5];
    while(1) {
        const startTime = Date.now();
        ballMovement(ball, scores);
        drawBall(ball)
        const EndTime = Date.now();
        elapsedTime = startTime - EndTime;
        await sleep(Math.max(0, TICK_RATE - (elapsedTime / 1000)) * 1000)
    }
}