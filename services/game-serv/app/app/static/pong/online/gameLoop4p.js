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
let p1 = new Player(0, 3.75);
let p2 = new Player(8.75, 3.75);
let p3 = new Player(3.75, 0);
let p4 = new Player(3.75, 8.75);
let ball = new Ball(4.5, 4.5);
let paddleMove = 0;
let loopBreaker = false;
let error = true;
let scores = [5, 5, 5, 5];
const roomName =  getRoomName();
function getRoomName() {
    let url =  window.location.pathname.split("/");
    return url[2];
}
// const gameWebSocket = new WebSocket(
//     'wss://'
//     + window.location.host
//     + '/ws/game/'
//     + roomName
//     + '/'
//     );
    
function startGame()
{
    gameWebSocket = new WebSocket(
        'wss://'
        + window.location.host
        + '/ws/game/'
        + roomName
        + '/4pong'
        );
    gameWebSocket.addEventListener("message", (event) => {
        msg = JSON.parse(event.data)
        switch (msg.type) {
            case "tick_data":
                UpdateGameData(msg);
                break;
            case "score_update":
                console.log(msg);
                UpdateScore(msg['scores']);
                break;
            case "game_end":
                GameEnd(msg['score'], msg['winner']);
                error = false;
                break;
            case "freeze":
                freeze(msg, gameWebSocket);
        }
    });
    gameWebSocket.addEventListener("close", (event) => {
        loopBreaker = true;
        popupType = document.getElementById("type");
        if (error == true) {
            popupType.innerText = "Game has crashed";
            modal.style.display = "flex";
        }
    })
}

function addPlayerToList(playerId, ul) {
    const element =  fetch("/api/player/" + playerId + "/html/")
    .then(data => {
        return data.text();
    })
    .then(html => {
        li = document.createElement('li')
        li.innerHTML = html
        ul.appendChild(li)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

async function freeze(msg) {
    state = msg.state;
    if (msg.state == true) {
        loopBreaker = true;
        if (msg.players.length) {
            modal = document.getElementById("modal");
            popupType = document.getElementById("type");
            popupMsg = document.getElementById("message");
            ul = document.getElementById('playersList')
            
            popupType.innerText = "Waiting for:";
            popupMsg.innerHTML = "Time out in <div id=\"timer\"></div>s";
            timer = document.getElementById("timer")
            ul.innerHTML = ''
            msg.players.forEach((player) => addPlayerToList(player, ul))
            let timeout = 60;
            timer.innerHTML = timeout;
            modal.style.display = "flex";
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
        modal = document.getElementById("modal")
        modal.style.display = "none";
        loopBreaker = false;
        await startAnimation();
        gameLoop(gameWebSocket);  
    }
}

document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowUp" || event.key == "ArrowLeft") {
        paddleMove = -1;
    } else if (event.key === "ArrowDown" || event.key == "ArrowRight") {
        paddleMove = 1;
    }
});

// document.addEventListener("keydown", (event) => {
//     let rightPaddle = document.getElementById("rightPaddle");
//     if (event.key === "ArrowLeft" && p2.y > 0) {
//         p2.y -= 0.25;
//     } else if (event.key === "ArrowRight" && p2.y < SIZE - PADDLE_SIZE) {
//         p2.y += 0.25;
//     }
//     rightPaddle.setAttribute("y", p2.y);
// });

function UpdateGameData(data) {
    p1 = data.P[0];
    p2 = data.P[1];
    p3 = data.P[2];
    p4 = data.P[3];
    ball = data.Ball;
}

function UpdateScore(score) {
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

function GameEnd(score, winner) {
    modal = document.getElementById("modal");
    type = document.getElementById("type");
    msg = document.getElementById("message");
    player = document.getElementById("playersList");
    if (score == 10)
        type.innerText = "Victory!"
    else
        type.innerText = "Defeat!"
    player.innerHTML = '';
    addPlayerToList(winner, player);
    msg.innerText = "has won!";
    modal.style.display = "flex";
}
// function hitPlayer(px, py, x, y) {
//     if ((x - BALL_SIZE == px + PADDLE_WIDTH && py <= y - BALL_SIZE && y - BALL_SIZE <= py + PADDLE_SIZE))
//         return true
//     if ((px == x + BALL_SIZE && py <= y + BALL_SIZE && y + BALL_SIZE <= py + PADDLE_SIZE))
//         return true
//     if ((px == x + BALL_SIZE && py <= y - BALL_SIZE && y - BALL_SIZE <= py + PADDLE_SIZE))
//         return true
//     if (x - BALL_SIZE == px + PADDLE_WIDTH && py <= y + BALL_SIZE && y + BALL_SIZE <= py + PADDLE_SIZE)
//         return true
//     return false
// }

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

function ballReachObstacle(ball, x, y) {
    if (scores[0] > 0 && willHitLeftPaddle(ball, p1.x, p1.y, x, y) == true) {
        ballHitPlayer(ball, 280, 160, y - p1.y);
        ball.speed += 0.1;
    }
    else if (scores[1] > 0 && willHitRightPaddle(ball, p2.x, p2.y, x, y) == true) {
        ballHitPlayer(ball, 260, -160, y - p2.y)
        ball.speed += 0.1;
    }
    else if (scores[2] > 0 && willHitTopPaddle(ball, p3.x, p3.y, x, y) == true) {
        ballHitPlayer(ball, 170, -160, x - p3.x)
        ball.speed += 0.1;
    }
    else if (scores[3] > 0 && willHitBottomPaddle(ball, p4.x, p4.y, x, y) == true) {
        ballHitPlayer(ball, 190, 160, x - p4.x)
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

function ballMovement(ball) {
    if (hitWall(ball.x) || hitWall(ball.y))
    {
        playersAreWall = true;
        if (hitWall(ball.x)) {
            if (scores[0] > 0 && ball.x - BALL_SIZE <= 0) {
                playersAreWall = false;
                ball.angle = 0;
            }
            else if (scores[1] > 0 && ball.x + BALL_SIZE >= SIZE) {
                playersAreWall = false;
                ball.angle = 180;
            }
        }
        else {
            if (scores[2] > 0 && ball.y - BALL_SIZE <= 0) {
                playersAreWall = false;
                ball.angle = 90;
            }
            else if (scores[3] > 0 && ball.y + BALL_SIZE >= SIZE) {
                playersAreWall = false;
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

    if (ballReachObstacle(ball, x, y) == true)
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

function drawPaddle() {
    let leftPaddle = document.getElementById("leftPaddle");
    let rightPaddle = document.getElementById("rightPaddle");
    let topPaddle = document.getElementById("topPaddle");
    let bottomPaddle = document.getElementById("bottomPaddle");
    if (scores[0] > 0)
        leftPaddle.setAttribute("y", p1.y);
    else
        leftPaddle.style.display = 'none';
    if (scores[1] > 0)
        rightPaddle.setAttribute("y", p2.y);
    else
        rightPaddle.style.display = 'none';
    if (scores[2] > 0)
        topPaddle.setAttribute("x", p3.x);
    else
        topPaddle.style.display = 'none';
    if (scores[3] > 0)
        bottomPaddle.setAttribute("x", p4.x);
    else
        bottomPaddle.style.display = 'none';
}

async function sendMove(gameWebSocket) {
    if (paddleMove != 0) {
        gameWebSocket.send(JSON.stringify({"type": "move", "paddleMove": paddleMove}))
        paddleMove = 0
    }
}

async function startAnimation() {
    let One = document.getElementById("1");
    let Two = document.getElementById("2");
    let Three = document.getElementById("3");
    let SVGBall = document.getElementById("ball");
    SVGBall.style.display = "none";
    Three.style.display = "block";
    await sleep(1000);
    Three.style.display = "none";
    Two.style.display = "block";
    await sleep(1000);
    Two.style.display = "none";
    One.style.display = "block";
    await sleep(1000);
    One.style.display = "none";
    SVGBall.style.display = "block";
}

async function gameLoop(gameWebSocket) {
    while(1) {
        const startTime = Date.now();
        ballMovement(ball)
        drawBall(ball)
        drawPaddle()
        sendMove(gameWebSocket)
        const EndTime = Date.now();
        elapsedTime = startTime - EndTime;
        await sleep(Math.max(0, TICK_RATE - (elapsedTime / 1000)) * 1000)
        if (loopBreaker === true)
            break;
    }
    loopBreaker = false;
}
startGame();