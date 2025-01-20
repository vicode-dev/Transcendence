function of3d4p_ballReachObstacle(ball, scores3dOf, x, y) {
    if (scores3dOf[0] > 0 && willHitLeftPaddle(ball, p1.x, p1.y, x, y) == true) {
        ballHitPlayer(ball, 280, 160, y - p1.y);
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (scores3dOf[1] > 0 && willHitRightPaddle(ball, p2.x, p2.y, x, y) == true) {
        ballHitPlayer(ball, 260, -160, y - p2.y)
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (scores3dOf[2] > 0 && willHitTopPaddle(ball, p3.x, p3.y, x, y) == true) {
        ballHitPlayer(ball, 170, -160, x - p3.x)
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (scores3dOf[3] > 0 && willHitBottomPaddle(ball, p4.x, p4.y, x, y) == true) {
        ballHitPlayer(ball, 190, 160, x - p4.x)
        if (ball.speed < MAX_SPEED)
            ball.speed += 0.1;
    }
    else if (willHitWall(x) == true) {
        if (ball.x < SIZE / 2) {
            ball.x = BALL_SIZE;
            if (scores3dOf[0] <= 0) {
                if (ball.angle % 90 == 0)
                ball.angle = 180 + ball.angle;
                else
                    ball.angle = (360 + 180 - ball.angle) % 360;
                }
            }
            else {
                ball.x = SIZE - BALL_SIZE;
                if (scores3dOf[1] <= 0) {
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
            if (scores3dOf[2] <= 0) {
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

function of3d4p_UpdateScore(score) {
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


function of3d4p_newPoint(scores3dOf, idx) {
    scores3dOf[idx] -= 1
    if (scores3dOf[idx] == 0) {
        switch (idx) {
            case 0:
                leftPaddle.visible = false;
                break;
            case 1:
                rightPaddle.visible = false;
                break;
            case 2:
                topPaddle.visible = false;
                break;
            case 3:
                bottomPaddle.visible = false;
                break;
            default:
                break;
            }
        }
    for (let i = 0; i < 4; i++) {
        if (i != idx && scores3dOf[i] <= 0 && scores3dOf[idx] == 0) {
            scores3dOf[i] -= 1;
        }
    }
    of3d4p_UpdateScore(scores3dOf);
}

function of3d4p_ballMovement(ball, scores3dOf) {
    if (hitWall(ball.x) || hitWall(ball.y))
    {
        let playersAreWall = true;
        if (hitWall(ball.x)) {
            if (scores3dOf[0] > 0 && ball.x - BALL_SIZE <= 0) {
                playersAreWall = false;
                of3d4p_newPoint(scores3dOf, 0);
                ball.angle = resetAngle(0, scores3dOf) + randomAngle();
            }
            else if (scores3dOf[1] > 0 && ball.x + BALL_SIZE >= SIZE) {
                playersAreWall = false;
                of3d4p_newPoint(scores3dOf, 1);
                ball.angle = resetAngle(1, scores3dOf) + randomAngle();
            }
        }
        else {
            if (scores3dOf[2] > 0 && ball.y - BALL_SIZE <= 0) {
                playersAreWall = false;
                of3d4p_newPoint(scores3dOf, 2);
                ball.angle = resetAngle(2, scores3dOf) + randomAngle();
            }
            else if (scores3dOf[3] > 0 && ball.y + BALL_SIZE >= SIZE) {
                playersAreWall = false;
                of3d4p_newPoint(scores3dOf, 3);
                ball.angle = resetAngle(3, scores3dOf) + randomAngle();
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

    if (of3d4p_ballReachObstacle(ball, scores3dOf, x, y) == true)
        return;
    ball.x = x;
    ball.y = y;

}

function of3d4p_generateScene(scene) {
	AddObjectToScene(scene, leftPaddle);
	AddObjectToScene(scene, rightPaddle);
    AddObjectToScene(scene, topPaddle, Math.PI / 2);
	AddObjectToScene(scene, bottomPaddle, Math.PI / 2);
	AddObjectToScene(scene, sphere);
	generateWalls(scene);
}

function clickDown3d4p(move, buttonId) {
    resetClick(buttonId);
    timers[buttonId] = setInterval(function() {
        if (move === "ArrowUp" && p2.y > PADDLE_WIDTH)
            p2.y -= 0.25;
        else if (move === "ArrowDown" && p2.y < SIZE - PADDLE_SIZE - PADDLE_WIDTH)
            p2.y += 0.25;
        else if (move === "w" && p1.y > PADDLE_WIDTH)
            p1.y -= 0.25;
        else if (move === "s" && p1.y < SIZE - PADDLE_SIZE - PADDLE_WIDTH)
            p1.y += 0.25;
        else if (move === "ArrowLeft" && p3.x > PADDLE_WIDTH)
            p3.x -= 0.25;
        else if (move === "ArrowRight" && p3.x < SIZE - PADDLE_SIZE - PADDLE_WIDTH)
            p3.x += 0.25;
        else if (move === "a" && p4.x > PADDLE_WIDTH)
            p4.x -= 0.25;
        else if (move === "d" && p4.x < SIZE - PADDLE_SIZE - PADDLE_WIDTH)
            p4.x += 0.25;
    }, 50);
}

function FourPlayerMovement(key) {
    if (key === "ArrowUp" && p2.y > PADDLE_WIDTH)
        p2.y -= 0.25;
    else if (key === "ArrowDown" && p2.y < SIZE - PADDLE_SIZE - PADDLE_WIDTH)
        p2.y += 0.25;
    else if (key === "w" && p1.y > PADDLE_WIDTH)
        p1.y -= 0.25;
    else if (key === "s" && p1.y < SIZE - PADDLE_SIZE - PADDLE_WIDTH)
        p1.y += 0.25;
    else if (key === "ArrowLeft" && p3.x > PADDLE_WIDTH)
        p3.x -= 0.25;
    else if (key === "ArrowRight" && p3.x < SIZE - PADDLE_SIZE - PADDLE_WIDTH)
        p3.x += 0.25;
    else if (key === "a" && p4.x > PADDLE_WIDTH)
        p4.x -= 0.25;
    else if (key === "d" && p4.x < SIZE - PADDLE_SIZE - PADDLE_WIDTH)
        p4.x += 0.25;
}

function of3d4p_GameEnd(scores) {
    // let box = document.getElementById("winner-msg");
    // let winner;

    // for (let i = 0; i < scores.length; i++) {
    //     if (scores[i] > 0) {
    //         winner = i + 1;
    //         break;
    //     }
    // }
    // box.innerText = "Player " + winner + " has won!";
    exitFullScreen();
}

function of3d4p_initPos() {
    let score1 = document.getElementById("score1");
    let score2 = document.getElementById("score2");
    let score3 = document.getElementById("score3");
    let score4 = document.getElementById("score4");

    // document.getElementById("winner-msg").innerText = '';
    score1.textContent = 5;
    score2.textContent = 5;
    score3.textContent = 5;
    score4.textContent = 5;
}

function of3d4p_victory(scores) {
    let count = 0;
    for (let i = 0; i < scores.length; i++) {
        if (scores[i] > 0)
            count++;
        if (count > 1)
            return false;
    }
    return true;
}

function of3d4p_movePaddle() {
    if (leftPaddle)
        leftPaddle.position.z = p1.y + PADDLE_SIZE / 2;
    if (rightPaddle)
        rightPaddle.position.z = p2.y + PADDLE_SIZE / 2;
    if (topPaddle)
        topPaddle.position.x = p3.x + PADDLE_SIZE / 2;
    if (bottomPaddle)
        bottomPaddle.position.x = p4.x + PADDLE_SIZE / 2;
}

async function of3d4p_gameLoop() {
    disableDoubleTapZoom();
    enterFullScreen();
    listenForScreenChange();
    blockContextMenu();

    root = document.documentElement;
    container = document.getElementById('center-div');
    style = getComputedStyle(root);
    background = style.getPropertyValue('--background-color').trim(); // Retrieve the CSS variable
    white = style.getPropertyValue('--secondary-color').trim(); // Retrieve the CSS variable
    yellow = style.getPropertyValue('--accent-color').trim(); // Retrieve the CSS variable
    pink = style.getPropertyValue('--accent-color').trim();
    scene = new THREE.Scene();
    renderer = new THREE.WebGLRenderer({ antialias: true });
    camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    // axesHelper = new THREE.AxesHelper(5); // The argument is the size of the axes
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
    ball = new Ball(4.5, 4.5, 195);
    p1 = new Player(0, 3.75);
    p2 = new Player(8.75, 3.75);
    p3 = new Player(3.75, 0);
    p4 = new Player(3.75, 8.75);
    let scores3dOf = [5, 5, 5, 5];
    setupScene();
	setupLight(scene);
	of3d4p_generateScene(scene);
    document.getElementById("start-btn").style.visibility = "hidden";
    destructors.push(of3d4p_destructor);
    of3d4p_initPos()

    window.addEventListener('resize', of3d4p_resizeEvent);
	while (1) {
        const startTime = Date.now();
        of3d4p_ballMovement(ball, scores3dOf);
        sphere.position.set(ball.x, 0.5, ball.y);
        of3d4p_movePaddle();
        renderer.render(scene, camera);
        const EndTime = Date.now();
        let elapsedTime = startTime - EndTime;
        await sleep(Math.max(0, TICK_RATE - (elapsedTime / 1000)) * 1000)
        if (of3d4p_victory(scores3dOf) == true)
            break;
    }
    of3d4p_GameEnd(scores3dOf);
    document.getElementById("start-btn").style.visibility = "visible";
    const canva = renderer.domElement;
    canva.parentNode.removeChild(canva);
    enableDoubleTapZoom();
    removeResizeListener();
}

function of3d4p_keydownEvent(event) {
    FourPlayerMovement(event.key);
    // if (event.key === "r")
    //     console.log(camera.position, printCameraRotationInDegrees(camera), camera.lookAt);
}

function of3d4p_resizeEvent() {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

function mainRendu3d4pOffline() {
    document.addEventListener("keydown", of3d4p_keydownEvent);
    // Disable pinch zoom
    document.addEventListener('gesturestart', preventDefaultHandler);
    document.addEventListener('gesturechange', preventDefaultHandler);
    document.addEventListener('gestureend', preventDefaultHandler);
    window.addEventListener("resize", resizeHandler);
}

function of3d4p_destructor() {
    // renderer.dispose(); //?
    p1 = null;
    p2 = null;
    p3 = null;
    p4 = null;
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
    topPaddle = null;
    bottomPaddle = null;
    sphere = null;
    scores3dOf = null;
    document.removeEventListener("keydown", of3d4p_keydownEvent);
    // Pinch Zoom
    document.removeEventListener('gesturestart', preventDefaultHandler);
    document.removeEventListener('gesturechange', preventDefaultHandler);
    document.removeEventListener('gestureend', preventDefaultHandler);
    window.removeEventListener('resize', of3d4p_resizeEvent);
    window.removeEventListener("resize", resizeHandler);
    enableDoubleTapZoom();
}

addMain(mainRendu3d4pOffline);
