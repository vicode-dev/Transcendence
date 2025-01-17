function of3d2p_ballReachObstacle(ball, x, y) {
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

function of3d2p_ballMovement(ball, scores) {
    if (hitWall(ball.x)) {
        if (ball.x - BALL_SIZE <= 0) {
            ball.angle = 0;
            scores[1] += 1;
        }
        else {
            ball.angle = 180;
            scores[0] += 1;
        }
        of3d2p_UpdateScore(scores);
        ball.x = 4.5;
        ball.y = 4.5;
        ball.speed = INIT_SPEED;
        return;
    }
    let x = ball.x + (Math.cos((Math.PI / 180) * ball.angle) / 8) * ball.speed;
    let y = ball.y + (Math.sin((Math.PI / 180) * ball.angle) / 8) * ball.speed;

    if (of3d2p_ballReachObstacle(ball, x, y) == true)
        return;
    ball.x = x;
    ball.y = y;

}

function of3d2p_generateScene(scene) {
	AddObjectToScene(scene, leftPaddle);
	AddObjectToScene(scene, rightPaddle);
	AddObjectToScene(scene, sphere);
	generateWalls(scene);
}

// function resetClick(buttonId) {
//     if (timers[buttonId]) {
//         clearInterval(timers[buttonId]);
//         delete timers[buttonId];
//     }
// }

function clickDown3d2p(move, buttonId) {
    resetClick(buttonId);
    timers[buttonId] = setInterval(function() {
        if (move === "ArrowUp" && p2.y > 0)
            p2.y -= 0.25;
        else if (move === "ArrowDown" && p2.y < SIZE - PADDLE_SIZE)
            p2.y += 0.25;
        else if (move === "w" && p1.y > 0)
            p1.y -= 0.25;
        else if (move === "s" && p1.y < SIZE - PADDLE_SIZE)
            p1.y += 0.25;
    }, 50);
}

function TwoPlayerMovement(key) {
    if (key === "ArrowUp" && p2.y > 0)
        p2.y -= 0.25;
    else if (key === "ArrowDown" && p2.y < SIZE - PADDLE_SIZE)
        p2.y += 0.25;
    else if (key === "w" && p1.y > 0)
        p1.y -= 0.25;
    else if (key === "s" && p1.y < SIZE - PADDLE_SIZE)
        p1.y += 0.25;
}

function of3d2p_UpdateScore(scores) {
    let score1 = document.getElementById("score1");
    let score2 = document.getElementById("score2");
    score1.textContent = scores[0];
    score2.textContent = scores[1];
}

function of3d2p_GameEnd(scores) {
    let box = document.getElementById("winner-msg");
    let winner;

    winner = scores[0] == 10 ? 1 : 2;
    box.innerText = "Player " + winner + " has won!";
    exitFullScreen();
}

function of3d2p_initPos() {
    let score1 = document.getElementById("score1");
    let score2 = document.getElementById("score2");

    document.getElementById("winner-msg").innerText = '';
    score1.textContent = 0;
    score2.textContent = 0;
}

async function of3d2p_gameLoop() {
    disableDoubleTapZoom();
    enterFullScreen();
    blockContextMenu();

    let scores = [0, 0];
    document.getElementById("start-btn").style.visibility = "hidden";
    // document.getElementById("rules").style.visibility = "visible";
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
    // axesHelper = new THREE.AxesHelper(5); // The argument is the size of the axes
    ambientLight = new THREE.AmbientLight(white, 0.6);
    directionalLight = new THREE.DirectionalLight(white, 0.8);
    leftWall = createWall({ position: new THREE.Vector3(- PADDLE_WIDTH / 2, 0.5, SIZE / 2) })
    rightWall = createWall({ position: new THREE.Vector3(SIZE + PADDLE_WIDTH / 2, 0.5, SIZE / 2) })
    topWall = createWall({ position: new THREE.Vector3(SIZE / 2, 0.5, - PADDLE_WIDTH / 2) })
    bottomWall = createWall({ position: new THREE.Vector3(SIZE / 2, 0.5, SIZE + PADDLE_WIDTH / 2) })
    pivot = new THREE.Object3D();

    window.addEventListener('resize', of3d2p_resizeEvent);


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
    ball = new Ball(4.5, 4.5, 180);
    p1 = new Player(0, 3.75);
    p2 = new Player(8.75, 3.75);
    setupScene();
	setupLight(scene);
	of3d2p_generateScene(scene);
    destructors.push(of3d2p_destructor);
    of3d2p_initPos();

	while (1) {
        const startTime = Date.now();
        of3d2p_ballMovement(ball, scores);
        sphere.position.set(ball.x, 0.5, ball.y);
        leftPaddle.position.z = p1.y + PADDLE_SIZE / 2;
        rightPaddle.position.z = p2.y + PADDLE_SIZE / 2;
        renderer.render(scene, camera);
        const EndTime = Date.now();
        let elapsedTime = startTime - EndTime;
        await sleep(Math.max(0, TICK_RATE - (elapsedTime / 1000)) * 1000)
        if (scores[0] == 10 || scores[1] == 10)
            break;
    }
    document.getElementById("start-btn").style.visibility = "visible";
    // document.getElementById("rules").style.visibility = "hidden";
    of3d2p_GameEnd(scores);
    const canva = renderer.domElement;
    canva.parentNode.removeChild(canva);
}

function of3d2p_keydownEvent(event) {
    TwoPlayerMovement(event.key);
    if (event.key === "r")
        console.log(camera.position, printCameraRotationInDegrees(camera), camera.lookAt);
}

function of3d2p_resizeEvent() {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

function mainRendu3d2pOffline() {
    //TODO
    // let leftArrowUp = document.getElementById("left-arrow-up");
    // leftArrowUp.addEventListener("pointerdown", move3dPlayer1Up);

    document.addEventListener("keydown", of3d2p_keydownEvent);
    // window.addEventListener('resize', of3d2p_resizeEvent);
}

function of3d2p_destructor() {
    p1 = null;
    p2 = null;
    ball = null;
    scene = null;
    renderer = null;
    camera = null;
    // axesHelper = null;
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
    document.removeEventListener("keydown", of3d2p_keydownEvent);
    document.removeEventListener("resize", of3d2p_resizeEvent);
}

addMain(mainRendu3d2pOffline);
