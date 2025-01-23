// const leftPaddle = createPaddle({
// 	position: new THREE.Vector3(PADDLE_WIDTH / 2, 0.5, SIZE / 2),
// 	color: yellow
// });
// const rightPaddle = createPaddle({
// 	position: new THREE.Vector3(SIZE - PADDLE_WIDTH, 0.5, SIZE / 2),
// 	color: yellow
// })
// const sphere = createBall({
// 	position: new THREE.Vector3(SIZE / 2, 0.5, SIZE / 2),
// 	radius: BALL_SIZE,
// 	color: pink
// })

async function on3d2p_freeze(msg, gameWebSocket) {
    showNavbar();
    navBarManualOverride = false;
    let state = msg.state
    if (msg.state == true) {
        loopBreaker = true;
        if (msg.players.length) {
            waitPopup();
            let ul = document.getElementById("playersList");
            let timer = document.getElementById("timer");
            let timeout = 60;
            msg.players.forEach((player) => addPlayerToList(player, ul))
            timer.innerHTML = timeout;
            while (state && timeout >= 0) {
                await sleep(1000);
                timeout--;
                timer.innerHTML = timeout;
            }
        }
    }
    else if (msg.state == false) {
        let modal = document.getElementById("modal");
        let popupMsg = document.getElementById("message");
        clearPopup();
        modal.style.display = "flex";
        for (let i = 3; i > 0; i--) {
            popupMsg.innerText = i;
            await sleep(1000);
        }
        modal.style.display = "none";
        loopBreaker = false;
        on3d2p_gameLoop(gameWebSocket);
    }
}

// window.addEventListener('resize', () => {
//     camera.aspect = container.clientWidth / container.clientHeight;
//     camera.updateProjectionMatrix();
//     renderer.setSize(container.clientWidth, container.clientHeight);
// });

function on3d2p_UpdateGameData(data) {
    p1 = data.P[0];
    p2 = data.P[1];
    ball = data.Ball;
}

function on3d2p_UpdateScore(data) {
    let score1 = document.getElementById("score1");
    let score2 = document.getElementById("score2");
    ball.angle = data.angle;
    score1.textContent = data.scores[0];
    score2.textContent = data.scores[1];
}

function on3d2p_GameEnd(score, winner) {
    showNavbar();
    navBarManualOverride = false;
    loopBreaker = true;
    if(on_index == null)
        endPopup("typeVictory", winner);
    else if (score[on_index] == 10)
        endPopup("typeVictory", winner);
    else
        endPopup("typeDefeat", winner);
    showNavbar();
}

function on3d2p_ballReachObstacle(ball, p1, p2, x, y) {
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

function on3d2p_ballMovement(ball, p1, p2) {
    if (hitWall(ball.x)) {
        // ball.angle = (ball.x - BALL_SIZE <= 0) ? 0 : 180;
        ball.x = 4.5;
        ball.y = 4.5;
        ball.speed = INIT_SPEED;
        return;
    }
    let x = ball.x + (Math.cos((Math.PI / 180) * ball.angle) / 8) * ball.speed;
    let y = ball.y + (Math.sin((Math.PI / 180) * ball.angle) / 8) * ball.speed;

    if (on3d2p_ballReachObstacle(ball, p1, p2, x, y) == true)
        return;
    ball.x = x;
    ball.y = y;

}

function on3d2p_generateScene(scene) {
	AddObjectToScene(scene, leftPaddle);
	AddObjectToScene(scene, rightPaddle);
	AddObjectToScene(scene, sphere);
	generateWalls(scene);
}

async function on3d2p_gameLoop(gameWebSocket) {
    hideNavbar();
    clearTimeout(inactivityTimeout);
    setupScene();
    setupLight(scene);
    on3d2p_generateScene(scene);
    while (1) {
        const startTime = Date.now();
        on3d2p_ballMovement(ball, p1, p2);
        sphere.position.set(ball.x, 0.5, ball.y);
        leftPaddle.position.z = p1.y + PADDLE_SIZE / 2;
        rightPaddle.position.z = p2.y + PADDLE_SIZE / 2;
        renderer.render(scene, camera);
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

function on3d2p_init(playersList) {
    let players = ["player1", "player2"];

    for (let i = 0; i < players.length; i++) {
        let name = document.getElementById(players[i]);
        name.src = "/api/player/" + playersList[i] + "/avatar/";
    }
}

function on3d2p_keydownEvent(event) {
    if (event.key === "ArrowUp") {
        paddleMove = -1;
    } else if (event.key === "ArrowDown") {
        paddleMove = 1;
    }
}

function on3d2p_closeEvent() {
    loopBreak = true;
    if (error == true) {
        crashPopup();
    }
}

function on3d2p_openEvent() {
    gameWebSocket.send(JSON.stringify({'type':'refresh'}))
    gameWebSocket.send(JSON.stringify({'type':'index'}));
}

function on3d2p_messageEvent(event) {
    let msg = JSON.parse(event.data)
    switch (msg.type) {
        case "init":
            on3d2p_init(msg["playersList"]);
            break;
        case "tick_data":
            on3d2p_UpdateGameData(msg);
            break;
        case "score_update":
            on3d2p_UpdateScore(msg);
            break;
        case "game_end":
            on3d2p_GameEnd(msg.score, msg.winner);
            error = false;
            break;
        case "freeze":
            on3d2p_freeze(msg, gameWebSocket);
            break;
        case "index":
            on_index = msg.index;
            break;
    }
}

function mainRendu3d2pOnline() {
    root = document.documentElement;
    style = getComputedStyle(root);
    background = style.getPropertyValue('--background-color').trim(); // Retrieve the CSS variable
    white = style.getPropertyValue('--secondary-color').trim(); // Retrieve the CSS variable
    yellow = style.getPropertyValue('--accent-color').trim(); // Retrieve the CSS variable
    pink = style.getPropertyValue('--accent-color').trim();
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
    sphere = createBall({
        position: new THREE.Vector3(SIZE / 2, 0.5, SIZE / 2),
        radius: BALL_SIZE,
        color: pink
    })

    loopBreaker = false;
    gameWebSocket = new WebSocket(`wss://${window.location.host}/ws/game/${document.querySelector('[name=gameId]').value}/2pong`);
    ball = new Ball(4.5, 4.5, 195);
    p1 = new Player(0, 3.75);
    p2 = new Player(8.75, 3.75);
    paddleMove = 0;
    error = true;
    destructors.push(on3d2p_destructor);
    gameWebSocket.addEventListener("message", on3d2p_messageEvent);
    gameWebSocket.addEventListener("close", on3d2p_closeEvent);
    gameWebSocket.addEventListener("open", on3d2p_openEvent);
    document.addEventListener("keydown", on3d2p_keydownEvent);
}

function on3d2p_destructor() {
    loopBreaker = true;
    p1 = null;
    p2 = null;
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
    sphere = null;
    document.removeEventListener("keydown", on3d2p_keydownEvent);
    gameWebSocket.removeEventListener("close", on3d2p_closeEvent);
    gameWebSocket.removeEventListener("open", on3d2p_openEvent);
    gameWebSocket.removeEventListener("message", on3d2p_messageEvent);
    enableDoubleTapZoom();
    unblockContextMenu();
    gameWebSocket.close();
}

addMain(mainRendu3d2pOnline);