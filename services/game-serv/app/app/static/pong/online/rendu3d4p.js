class Ball {
	constructor(x, y, angle) {
		this.x = x;
		this.y = y;
		this.angle = angle;
		this.speed = 1; // Adjust speed as needed
	}
}

class Player {
	constructor(x, y) {
		this.x = x;
		this.y = y;
	}
}

const SIZE = 9;
const PADDLE_SIZE = 1.5;
const PADDLE_WIDTH = 0.25;
const BALL_SIZE = 0.125;
const TICK_RATE = 1 / 20;
const MAX_SPEED = 10;

const root = document.documentElement;
const style = getComputedStyle(root);
const background = style.getPropertyValue('--background-color').trim(); // Retrieve the CSS variable
const white = style.getPropertyValue('--secondary-color').trim(); // Retrieve the CSS variable
const yellow = style.getPropertyValue('--accent-color').trim(); // Retrieve the CSS variable
const pink = style.getPropertyValue('--secondary-color').trim();
const scene = new THREE.Scene();
const renderer = new THREE.WebGLRenderer({ antialias: true });
const container = document.getElementById('center-div');
const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
const axesHelper = new THREE.AxesHelper(5); // The argument is the size of the axes
const ambientLight = new THREE.AmbientLight(white, 0.6);
const directionalLight = new THREE.DirectionalLight(white, 0.8);


let p1 = new Player(0, 3.75);
let p2 = new Player(8.75, 3.75);
let p3 = new Player(3.75, 0);
let p4 = new Player(3.75, 8.75);
let ball = new Ball(4.5, 4.5, 0);
let scores = [5, 5, 5, 5];
const leftPaddle = createPaddle({
	position: new THREE.Vector3(PADDLE_WIDTH / 2, 0.5, SIZE / 2),
	color: yellow
});
const rightPaddle = createPaddle({
	position: new THREE.Vector3(SIZE - PADDLE_WIDTH / 2, 0.5, SIZE / 2),
	color: yellow
})
const topPaddle = createPaddle({
	position: new THREE.Vector3(SIZE / 2, 0.5, PADDLE_WIDTH / 2),
	color: yellow
})
const bottomPaddle = createPaddle({
	position: new THREE.Vector3(SIZE / 2, 0.5, SIZE - PADDLE_WIDTH / 2),
	color: yellow
})
const sphere = createBall({
	position: new THREE.Vector3(SIZE / 2, 0.5, SIZE / 2),
	radius: BALL_SIZE,
	color: pink
})
const leftWall = createWall({ position: new THREE.Vector3(- PADDLE_WIDTH / 2, 0.5, SIZE / 2) })
const rightWall = createWall({ position: new THREE.Vector3(SIZE + PADDLE_WIDTH / 2, 0.5, SIZE / 2) })
const topWall = createWall({ position: new THREE.Vector3(SIZE / 2, 0.5, - PADDLE_WIDTH / 2) })
const bottomWall = createWall({ position: new THREE.Vector3(SIZE / 2, 0.5, SIZE + PADDLE_WIDTH / 2) })

function createBoxGeometry({ position, size, color = 0xffffff } = {}) {
	const geometry = new THREE.BoxGeometry(size.x, size.y, size.z);
	const material = new THREE.MeshBasicMaterial({ color });
	const box = new THREE.Mesh(geometry, material);
	box.position.copy(position);
	return box;
}

function createPaddle({ position, color = 0xffffff } = {}) {
	return createBoxGeometry({ position, size: new THREE.Vector3(PADDLE_WIDTH, 0.2, PADDLE_SIZE), color });
}

function createWall({ position }) {
	return createBoxGeometry({ position, size: new THREE.Vector3(PADDLE_WIDTH, 0.5, SIZE + PADDLE_WIDTH), pink });
}

function createBall({ position, radius, color = 0xffffff } = {}) {
	const geometry = new THREE.SphereGeometry(radius, 32, 32);
	const material = new THREE.MeshStandardMaterial({ color });
	const ball = new THREE.Mesh(geometry, material);
	ball.position.copy(position);
	return ball;
}


// function getRoomName() {
//     let url = window.location.href;
//     let pathSegments = url.split('/').filter(Boolean);
//     return pathSegments[pathSegments.length - 1];
// }

// function main() {
//     gameWebSocket = new WebSocket(`wss://${window.location.host}/ws/game/${getRoomName()}/2pong`);
//     gameWebSocket.addEventListener("message", (event) => {
//         msg = JSON.parse(event.data)
//         switch (msg.type) {
//             case "tick_data":
//                 console.log(msg);
//                 // UpdateGameData(msg);
//                 break;
//             case "score_update":
//                 // UpdateScore(msg);
//                 break;
//             case "game_end":
//                 // GameEnd(msg['score'], msg['winner']);
//                 error = false;
//                 break;
//             case "freeze":
//                 // freeze(msg, gameWebSocket);
//         }
//     });
//     gameWebSocket.addEventListener("close", (event) => {
//         // loopBreak = true;
//         // popupType = document.getElementById("type");
//         // if (error == true) {
//         //     popupType.innerText = "Game has crashed";
//         //     modal.style.display = "flex";
//         // }
//     }
//     );
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
    ball.angle = (360 + startAngle + (diff / (PADDLE_SIZE + 2 * BALL_SIZE)) * (ballPos + BALL_SIZE)) % 360
}

function ballReachObstacle(ball, p1, p2, x, y) {
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
    // UpdateScore(scores);
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



function AddObjectToScene(scene, object, rotation = null) {
	if (rotation) {
		object.rotation.y = rotation;
	}
	scene.add(object);
}

function generateWalls(scene) {
	AddObjectToScene(scene, topWall, Math.PI / 2);
	AddObjectToScene(scene, bottomWall, Math.PI / 2);
	AddObjectToScene(scene, leftWall);
	AddObjectToScene(scene, rightWall);
}

function generateScene(scene) {
	AddObjectToScene(scene, leftPaddle);
	AddObjectToScene(scene, rightPaddle);
    AddObjectToScene(scene, topPaddle, Math.PI / 2);
	AddObjectToScene(scene, bottomPaddle, Math.PI / 2);
	AddObjectToScene(scene, sphere);
	generateWalls(scene);
}

function setupScene() {
	renderer.setSize(container.clientWidth, container.clientHeight);
	renderer.shadowMap.enabled = true;
	container.appendChild(renderer.domElement);
}

const pivot = new THREE.Object3D();
function rotateCamera() {
	pivot.rotation.y = degreesToRadians(-0.09711639542445165);
	pivot.rotation.x = degreesToRadians(-56.98787474114721);
	pivot.rotation.z = degreesToRadians(-0.14947646093265465);
	//pivot.rotation.x += angle;
}

function setupLight(scene) {
	scene.background = new THREE.Color(background);
	directionalLight.position.set(5, 5, 5);
	directionalLight.castShadow = true;
	axesHelper.position.y = 0;
	AddObjectToScene(scene, ambientLight);
	AddObjectToScene(scene, directionalLight);
	AddObjectToScene(scene, axesHelper);
	scene.add(pivot);
	pivot.add(camera);
	camera.position.set(4.337915334242398, 14.944152324169096, 14.401552868816939);
	camera.lookAt(SIZE / 2, 0, SIZE / 2);
}

function animate() {
	requestAnimationFrame(animate);
	ballMovement(ball, scores);
	sphere.position.set(ball.x, 0.5, ball.y);
	leftPaddle.position.z = p1.y + PADDLE_SIZE / 2;
	rightPaddle.position.z = p2.y + PADDLE_SIZE / 2;
    topPaddle.position.x = p3.x + PADDLE_SIZE / 2;
	bottomPaddle.position.x = p4.x + PADDLE_SIZE / 2;
	renderer.render(scene, camera);
}

function PlayerMovement(key) {
	if (key === "ArrowUp" && p2.y > 0 && scores[1] > 0) 
        p2.y -= 0.25;
	else if (key === "ArrowDown" && p2.y < SIZE - PADDLE_SIZE && scores[1] > 0) 
        p2.y += 0.25;
	else if (key === "w" && p1.y > 0 && scores[0] > 0)
        p1.y -= 0.25;
	else if (key === "s" && p1.y < SIZE - PADDLE_SIZE && scores[0] > 0)
        p1.y += 0.25;
    else if (key === "ArrowLeft" && p3.x > 0 && scores[2] > 0) 
        p3.x -= 0.25;
	else if (key === "ArrowRight" && p3.x < SIZE - PADDLE_SIZE && scores[2] > 0) 
        p3.x += 0.25;
	else if (key === "a" && p4.x > 0 && scores[3] > 0)
        p4.x -= 0.25;
	else if (key === "d" && p4.x < SIZE - PADDLE_SIZE && scores[3] > 0) 
        p4.x += 0.25;
}

function printCameraRotationInDegrees(camera) {
    console.log('Camera Rotation:');
    console.log('X:', radiansToDegrees(camera.rotation.x));
    console.log('Y:', radiansToDegrees(camera.rotation.y));
    console.log('Z:', radiansToDegrees(camera.rotation.z));
}

async function gameLoop() {
    setupScene();
	setupLight(scene);
	generateScene(scene);
	document.addEventListener("keydown", (event) => {
        PlayerMovement(event.key);
        if (event.key === "r")
		console.log(camera.position, printCameraRotationInDegrees(camera), camera.lookAt);
	});
	animate();
	window.addEventListener('resize', () => {
		camera.aspect = container.clientWidth / container.clientHeight;
		camera.updateProjectionMatrix();
		renderer.setSize(container.clientWidth, container.clientHeight);
	});
}
