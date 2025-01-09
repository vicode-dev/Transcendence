let scores3d;

async function on3d4p_freeze(msg) {
    let state = msg.state;
    if (msg.state == true) {
        loopBreaker = true;
        if (msg.players.length) {
            waitPopup();
            let ul = document.getElementById("playersList");
            let timer = document.getElementById("timer");
            let timeout = 60;
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
        let popupMsg = document.getElementById("message");
        clearPopup();
        modal.style.display = "flex";
        for (let i = 3; i > 0; i--) {
            popupMsg.innerText = i;
            await sleep(1000);
        }
        modal.style.display = "none";
        loopBreaker = false;
        on3d4p_gameLoop(gameWebSocket);  
    }
}

function on3d4p_UpdateGameData(data) {
    p1 = data.P[0];
    p2 = data.P[1];
    p3 = data.P[2];
    p4 = data.P[3];
    ball = data.Ball;
}

function on3d4p_UpdateScore(score) {
    let score1 = document.getElementById("score1");
    let score2 = document.getElementById("score2");
    let score3 = document.getElementById("score3");
    let score4 = document.getElementById("score4");
    scores3d = score;
    if (score[0] >= 0)
        score1.textContent = score[0];
    if (score[1] >= 0)
        score2.textContent = score[1];
    if (score[2] >= 0)
        score3.textContent = score[2];
    if (score[3] >= 0)
        score4.textContent = score[3];
}

function on3d4p_GameEnd(score, winner) {
    if (score == 1)
        endPopup("typeVictory", winner);
    else
        endPopup("typeDefeat", winner);
}

function on3d4p_ballReachObstacle(ball, scores3d, x, y) {
    if (scores3d[0] > 0 && willHitLeftPaddle(ball, p1.x, p1.y, x, y) == true) {
        ballHitPlayer(ball, 280, 160, y - p1.y);
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (scores3d[1] > 0 && willHitRightPaddle(ball, p2.x, p2.y, x, y) == true) {
        ballHitPlayer(ball, 260, -160, y - p2.y)
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (scores3d[2] > 0 && willHitTopPaddle(ball, p3.x, p3.y, x, y) == true) {
        ballHitPlayer(ball, 170, -160, x - p3.x)
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (scores3d[3] > 0 && willHitBottomPaddle(ball, p4.x, p4.y, x, y) == true) {
        ballHitPlayer(ball, 190, 160, x - p4.x)
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (willHitWall(x) == true) {
        if (ball.x < SIZE / 2) {
            ball.x = BALL_SIZE;
            if (scores3d[0] <= 0) {
                if (ball.angle % 90 == 0)
                ball.angle = 180 + ball.angle;
                else
                    ball.angle = (360 + 180 - ball.angle) % 360;
                }
            }
            else {
                ball.x = SIZE - BALL_SIZE;
                if (scores3d[1] <= 0) {
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
            if (scores3d[2] <= 0) {
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

function on3d4p_newPoint(scores3d, idx) {
    scores3d[idx] -= 1
    for (let i = 0; i < 4; i++) {
        if (i != idx && scores3d[i] <= 0 && scores3d[idx] == 0) {
            scores3d[i] -= 1;
        }
    }
    on3d4p_UpdateScore(scores3d);
}

function on3d4p_ballMovement(ball, scores3d) {
    if (hitWall(ball.x) || hitWall(ball.y))
    {
        let playersAreWall = true;
        if (hitWall(ball.x)) {
            if (scores3d[0] > 0 && ball.x - BALL_SIZE <= 0) {
                playersAreWall = false;
                on3d4p_newPoint(scores3d, 0);
                ball.angle = resetAngle(0, scores3d);
            }
            else if (scores3d[1] > 0 && ball.x + BALL_SIZE >= SIZE) {
                playersAreWall = false;
                on3d4p_newPoint(scores3d, 1);
                ball.angle = 180;
            }
        }
        else {
            if (scores3d[2] > 0 && ball.y - BALL_SIZE <= 0) {
                playersAreWall = false;
                on3d4p_newPoint(scores3d, 2);
                ball.angle = 90;
            }
            else if (scores3d[3] > 0 && ball.y + BALL_SIZE >= SIZE) {
                playersAreWall = false;
                on3d4p_newPoint(scores3d, 3);
                ball.angle = 270;
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

    if (on3d4p_ballReachObstacle(ball, scores3d, x, y) == true)
        return;
    ball.x = x;
    ball.y = y;
    
}

function on3d4p_generateScene(scene) {
	AddObjectToScene(scene, leftPaddle);
	AddObjectToScene(scene, rightPaddle);
    AddObjectToScene(scene, topPaddle, Math.PI / 2);
	AddObjectToScene(scene, bottomPaddle, Math.PI / 2);
	AddObjectToScene(scene, sphere);
	generateWalls(scene);
}

async function on3d4p_gameLoop() {
    setupScene();
	setupLight(scene);
	on3d4p_generateScene(scene);
    while (1) {
        const startTime = Date.now();
        on3d4p_ballMovement(ball, scores3d);
        sphere.position.set(ball.x, 0.5, ball.y);
        leftPaddle.position.z = p1.y + PADDLE_SIZE / 2;
        rightPaddle.position.z = p2.y + PADDLE_SIZE / 2;
        topPaddle.position.x = p3.x + PADDLE_SIZE / 2;
        bottomPaddle.position.x = p4.x + PADDLE_SIZE / 2;
        renderer.render(scene, camera);
        sendMove(gameWebSocket);
        const EndTime = Date.now();
        elapsedTime = startTime - EndTime;
        await sleep(Math.max(0, TICK_RATE - (elapsedTime / 1000)) * 1000)
        if (loopBreaker === true)
            break;
    }
    loopBreaker = false;
	// window.addEventListener('resize', () => {
	// 	camera.aspect = container.clientWidth / container.clientHeight;
	// 	camera.updateProjectionMatrix();
	// 	renderer.setSize(container.clientWidth, container.clientHeight);
	// });
}

function on3d4p_keydownEvent(event) {
    if (event.key === "ArrowUp" || event.key == "ArrowLeft") {
        paddleMove = -1;
    } else if (event.key === "ArrowDown" || event.key == "ArrowRight") {
        paddleMove = 1;
    }
}

function on3d4p_init(msg) {
    let playersList = msg["playersList"];
    let players = ["player1", "player2", "player3", "player4"];

    for (let i = 0; i < players.length; i++) {
        let name = document.getElementById(players[i]);
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

function on3d4p_closeEvent() {
    loopBreak = true;
    if (error == true) {
        crashPopup();
    }
}

function on3d4p_openEvent() {
    gameWebSocket.send(JSON.stringify({'type':'refresh'}));
}

function on3d4p_messageEvent(event) {
    let msg = JSON.parse(event.data)
    switch (msg.type) {
        case "init":
            on3d4p_init(msg);
            break;
        case "tick_data":
            on3d4p_UpdateGameData(msg);
            break;
        case "score_update":
            on3d4p_UpdateScore(msg['scores']);
            break;
        case "game_end":
            on3d4p_GameEnd(msg['score'], msg['winner']);
            error = false;
            break;
        case "freeze":
            on3d4p_freeze(msg, gameWebSocket);
    }
}

function mainRendu3d4pOnline() {
    root = document.documentElement;
    style = getComputedStyle(root);
    background = style.getPropertyValue('--background-color').trim(); // Retrieve the CSS variable
    white = style.getPropertyValue('--secondary-color').trim(); // Retrieve the CSS variable
    yellow = style.getPropertyValue('--accent-color').trim(); // Retrieve the CSS variable
    pink = style.getPropertyValue('--secondary-color').trim();
    scene = new THREE.Scene();
    renderer = new THREE.WebGLRenderer({ antialias: true });
    container = document.getElementById('center-div');
    camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    axesHelper = new THREE.AxesHelper(5); // The argument is the size of the axes
    ambientLight = new THREE.AmbientLight(white, 0.6);
    directionalLight = new THREE.DirectionalLight(white, 0.8);
    leftWall = createWall({ position: new THREE.Vector3(- PADDLE_WIDTH / 2, 0.5, SIZE / 2) })
    rightWall = createWall({ position: new THREE.Vector3(SIZE + PADDLE_WIDTH / 2, 0.5, SIZE / 2) })
    topWall = createWall({ position: new THREE.Vector3(SIZE / 2, 0.5, - PADDLE_WIDTH / 2) })
    bottomWall = createWall({ position: new THREE.Vector3(SIZE / 2, 0.5, SIZE + PADDLE_WIDTH / 2) })
    pivot = new THREE.Object3D();

    leftPaddle = createPaddle({
        position: new THREE.Vector3(PADDLE_WIDTH / 2, 0.5, SIZE / 2),
        color: yellow
    });
    rightPaddle = createPaddle({
        position: new THREE.Vector3(SIZE - PADDLE_WIDTH / 2, 0.5, SIZE / 2),
        color: yellow
    })
    topPaddle = createPaddle({
        position: new THREE.Vector3(SIZE / 2, 0.5, PADDLE_WIDTH / 2),
        color: yellow
    })
    bottomPaddle = createPaddle({
        position: new THREE.Vector3(SIZE / 2, 0.5, SIZE - PADDLE_WIDTH / 2),
        color: yellow
    })
    sphere = createBall({
        position: new THREE.Vector3(SIZE / 2, 0.5, SIZE / 2),
        radius: BALL_SIZE,
        color: pink
    })
    ball = new Ball(4.5, 4.5, 180);
    p1 = new Player(0, 3.75);
    p2 = new Player(8.75, 3.75);
    p3 = new Player(3.75, 0);
    p4 = new Player(3.75, 8.75);
    scores3d = [5, 5, 5, 5];
    paddleMove = 0;
    loopBreaker = false;
    error = true;
    gameWebSocket = new WebSocket(`wss://${window.location.host}/ws/game/${document.querySelector('[name=gameId]').value}/4pong`);
    destructors.push(on3d4p_destructor);
    gameWebSocket.addEventListener("message", on3d4p_messageEvent);
    gameWebSocket.addEventListener("close", on3d4p_closeEvent);
    gameWebSocket.addEventListener("open", on3d4p_openEvent);
    document.addEventListener("keydown", on3d4p_keydownEvent);
}

function on3d4p_destructor() {
    p1 = null;
    p2 = null;
    p3 = null;
    p4 = null;
    ball = null;
    scene = null;
    renderer = null;
    camera = null;
    axesHelper = null;
    ambientLight = null;
    directionalLight = null;
    leftWall = null;
    rightWall = null;
    topWall = null;
    bottomWall = null;
    pivot = null;
    leftPaddle = null;
    rightPaddle = null;
    topPaddle = null;
    bottomPaddle = null;
    sphere = null;
    scores3d = null;
    document.removeEventListener("keydown", on3d4p_keydownEvent);
    gameWebSocket.removeEventListener("close", on3d4p_closeEvent);
    gameWebSocket.removeEventListener("open", on3d4p_openEvent);
    gameWebSocket.removeEventListener("message", on3d4p_messageEvent);
    gameWebSocket.close();
}

addMain(mainRendu3d4pOnline);