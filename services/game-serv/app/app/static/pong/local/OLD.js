// OFFLINE 2P

// document.addEventListener("DOMContentLoaded", () => {
//     console.log('loaded');
//     fullScreen();
// })
// document.getElementById('start-btn').style.display = 'none';

function fullScreen() {
    if(screen.width <= 400) {
        if (!document.fullscreenElement) {
            if (document.documentElement.requestFullscreen) {
                document.documentElement.requestFullscreen();
            } else if (document.documentElement.webkitRequestFullscreen) {
                document.documentElement.webkitRequestFullscreen();
            } else if (document.documentElement.msRequestFullscreen) {
                document.documentElement.msRequestFullscreen();
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
            }
        }
    }
}

// class Ball {

//     constructor(x, y, angle) {
//         this.x = x;
//         this.y = y;
//         this.angle = 180;
//         this.speed = 1;
//     }
// }

// class Player {

//     constructor(x, y) {
//         this.y = y;
//         this.x = x;

//     }
// }

// const SIZE = 9;
// const PADDLE_SIZE = 1.5;
// const PADDLE_WIDTH = 0.25;
// const BALL_SIZE = 0.125;
// const TICK_RATE = 1/20;
// const MAX_SPEED = 10;
let p1 = new Player(0, 3.75);
let p2 = new Player(8.75, 3.75);

document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowUp" || event.key === "ArrowDown") {
        moveLeftPaddle(event.key);
    }
    else if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
        moveRightPaddle(event.key);
    }
});

function moveLeftPaddle(move) {
    let leftPaddle = document.getElementById("leftPaddle");
    if (!leftPaddle)
        return ;
    if (move === "ArrowUp" && p1.y > 0) {
        p1.y -= 0.25;
    } else if (move === "ArrowDown" && p1.y < SIZE - PADDLE_SIZE) {
        p1.y += 0.25;
    }
    leftPaddle.setAttribute("y", p1.y);
}

function moveRightPaddle(move) {
    let rightPaddle = document.getElementById("rightPaddle");
    if (!rightPaddle)
        return ;
    if (move === "ArrowLeft" && p2.y > 0) {
        p2.y -= 0.25;
    } else if (move === "ArrowRight" && p2.y < SIZE - PADDLE_SIZE) {
        p2.y += 0.25;
    }
    rightPaddle.setAttribute("y", p2.y);
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
    fullScreen();

    document.getElementById("start-btn").style.display = "none";
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
    document.getElementById("start-btn").style.display = "block";
    GameEnd(scores);
}
















// OFFLINE 4P
// class Ball {

//     constructor(x, y, angle) {
//         this.x = x;
//         this.y = y;
//         this.angle = 180;
//         this.speed = 1;
//     }
// }

// class Player {

//     constructor(x, y) {
//         this.y = y;
//         this.x = x;

//     }
// }

// const SIZE = 9;
// const PADDLE_SIZE = 1.5;
// const PADDLE_WIDTH = 0.25;
// const BALL_SIZE = 0.125;
// const TICK_RATE = 1/20;
// const MAX_SPEED = 10;
// let p1 = new Player(0, 3.75);
// let p2 = new Player(8.75, 3.75);
// let p3 = new Player(3.75, 0);
// let p4 = new Player(3.75, 8.75);

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















// OFFLINE 2/4P 3D

/* GLobal constants*/
const centerField = 4.5;
const floatEffect = 0.5;
const paddleHeight = 1.5;
const paddleWidth = 0.25;
const paddleDepth = 0.2;
const p1StartX = 0;
const p1StartY = centerField;
const p2StartX = 8.75;
const p2StartY = centerField;
const p3StartX = centerField;
const p3StartY = 0;
const p4StartX = centerField;
const p4StartY = 8.75;
// const yellow = 0xffff00;
// const pink = 0xe070d0;
// const white = 0xffffff;
//const background = 0x2d3247;
const root = document.documentElement;
const style = getComputedStyle(root);
const background = style.getPropertyValue('--background-color').trim(); // Retrieve the CSS variable
const white = style.getPropertyValue('--secondary-color').trim(); // Retrieve the CSS variable
const yellow = style.getPropertyValue('--accent-color').trim(); // Retrieve the CSS variable
const pink = style.getPropertyValue('--secondary-color').trim(); // Retrieve the CSS variable
const radius = 0.125;
const heightSegments = 32;
const widthSegments = heightSegments;
const wallHeight = 0.5;
const wallDepth = paddleWidth;
const wallLength = 10.75;
const speed = 0.25;
const distance = 1;
const scene = new THREE.Scene();
const renderer = new THREE.WebGLRenderer({ antialias: true });
const container = document.getElementById('center-div');
const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
const ambientLight = new THREE.AmbientLight(white, 0.6);
const directionalLight = new THREE.DirectionalLight(white, 0.8);
const maxPlayers = container.dataset.maxPlayers;
const axesHelper = new THREE.AxesHelper(5); // The argument is the size of the axes
const sensitivity = 130;

// --- Game Logic Classes ---
// class Ball {
// 	constructor(x, y, angle) {
// 		this.x = x;
// 		this.y = y;
// 		this.angle = angle;
// 		this.speed = 0.1; // Adjust speed as needed
// 	}
// }

// class Player {
// 	constructor(x, y) {
// 		this.x = x;
// 		this.y = y;
// 		this.score = 0; // Keep track of the player's score
// 	}
// }

function createBoxGeometry({ position, size, color = 0xffffff } = {}) {
	const geometry = new THREE.BoxGeometry(size.x, size.y, size.z);
	const material = new THREE.MeshBasicMaterial({ color });
	const box = new THREE.Mesh(geometry, material);
	box.position.copy(position);
	return box;
}

function createPaddle({ position, color = 0xffffff } = {}) {
	return createBoxGeometry({ position, size: new THREE.Vector3(paddleWidth, paddleDepth, paddleHeight), color });
}

function createWall({ position }) {
	return createBoxGeometry({ position, size: new THREE.Vector3(wallDepth, wallHeight, wallLength), white });
}

function createBall({ position, radius, color = 0xffffff } = {}) {
	const geometry = new THREE.SphereGeometry(radius, widthSegments, heightSegments);
	const material = new THREE.MeshStandardMaterial({ color });
	const ball = new THREE.Mesh(geometry, material);
	ball.position.copy(position);
	return ball;
}

/* Players*/
// const p1 = new Player(p1StartX, p1StartY);
const leftPaddle = createPaddle({
	position: new THREE.Vector3(p1StartX, floatEffect, p1StartY),
	color: yellow
});

// const p2 = new Player(p2StartX, p2StartY);
const rightPaddle = createPaddle({
	position: new THREE.Vector3(p2StartX, floatEffect, p2StartY),
	color: yellow
})

const p3 = new Player(p3StartX, p3StartY);
const topPaddle = createPaddle({
	position: new THREE.Vector3(p3StartX, floatEffect, p3StartY),
	color: yellow
})

const p4 = new Player(p4StartX, p4StartY);
const bottomPaddle = createPaddle({
	position: new THREE.Vector3(p4StartX, floatEffect, p4StartY),
	color: yellow
})

/* Ball*/
const ball = new Ball(centerField, centerField, Math.PI);
const sphere = createBall({
	position: new THREE.Vector3(centerField, floatEffect, centerField),
	radius: radius,
	color: pink
})

/* Walls */
const leftWall = createWall({ position: new THREE.Vector3(p1StartX - distance, wallHeight, centerField) })
const rightWall = createWall({ position: new THREE.Vector3(p2StartX + distance, wallHeight, centerField) })
const topWall = createWall({ position: new THREE.Vector3(centerField, wallHeight, p3StartY - distance) })
const bottomWall = createWall({ position: new THREE.Vector3(centerField, wallHeight, p4StartY + distance) })

// --- Game Logic Math ---
function resetBall(ball, angle) {
	// Calculate the ball's new position
	ball.speed = 0.1; // Reset ball speed
	ball.x = centerField;
	ball.y = centerField;
	ball.angle = angle;
}

function degreesToRadians(angle) {
	return angle * (Math.PI / 180);
}

function isBallHittingPaddle(ballMesh, paddleMesh) {
	const ballWorldPosition = new THREE.Vector3();
	ballMesh.getWorldPosition(ballWorldPosition);

	const ballRadius = ballMesh.geometry.parameters.radius * ballMesh.scale.x; // Account for scaling
	const ballBoundingSphere = new THREE.Sphere(ballWorldPosition, ballRadius);
	const paddleBoundingBox = new THREE.Box3().setFromObject(paddleMesh);

	// Check if the ball intersects with the paddle
	const isHitting = paddleBoundingBox.intersectsSphere(ballBoundingSphere);
	if (isHitting) {
		// Calculate the relative hit position (-1 is left/top, 0 is center, +1 is right/bottom)
		const paddleCenter = paddleMesh.position.clone();
		let relativeHitPosition = (ballWorldPosition.z - paddleCenter.z) / (paddleHeight / 2); // For vertical paddles
		// Invert the relative hit position for the right paddle
		if (paddleMesh.position.x > 0) { // Assuming right paddle has positive x position
			relativeHitPosition = -relativeHitPosition;
		}

		return { isHitting: true, relativeHitPosition: THREE.MathUtils.clamp(relativeHitPosition, -1, 1) };
	}
	return { isHitting: false, relativeHitPosition: 0 };
}

function playerCollision(sphere, paddle) {
	const collision = isBallHittingPaddle(sphere, paddle);
	if (collision.isHitting) {
		// Reflect ball's angle based on hit position
		const relativeHitPosition = collision.relativeHitPosition;
		// Change the ball's angle based on how far from the center it hit (steeper bounce for edges)
		ball.angle = 180 + ball.angle + relativeHitPosition * sensitivity;
		return true;
	}
	return false;
}


function wallCollision(sphere) {
	if (isBallHittingPaddle(sphere, leftWall).isHitting)
		resetBall(ball, 0);
	else if (isBallHittingPaddle(sphere, rightWall).isHitting)
		resetBall(ball, 180);
	else if (maxPlayers == 4 && isBallHittingPaddle(sphere, topWall).isHitting)
		resetBall(ball, 90);
	else if (maxPlayers == 4 && isBallHittingPaddle(sphere, bottomWall).isHitting)
		resetBall(ball, 270);
	else {
		if (isBallHittingPaddle(sphere, topWall).isHitting)
			ball.y = ball.y + wallDepth;
		else if (isBallHittingPaddle(sphere, bottomWall).isHitting)
			ball.y = ball.y - wallDepth;
		else
			return false;
		ball.angle = -ball.angle;
	}
	return true;
}

function ballMovement(ball) {
	// Check for player collisions
	if (playerCollision(sphere, leftPaddle)) {
		ball.x = paddleWidth;
	}
	if (playerCollision(sphere, rightPaddle)) {
		ball.x = p2StartX - paddleWidth;
	}
	if (maxPlayers == 4) {
		if (playerCollision(sphere, topPaddle)) {
			ball.y = paddleWidth;
		}
		if (playerCollision(sphere, bottomPaddle)) {
			ball.y = p4StartY - paddleWidth;
		}
	}

	// Calculate the ball's new position
	let y = ball.y + Math.sin(degreesToRadians(ball.angle)) * ball.speed;
	let x = ball.x + Math.cos(degreesToRadians(ball.angle)) * ball.speed;
	// Check for wall collisions
	if (!wallCollision(sphere)) {
		ball.x = x;
		ball.y = y;
	}
}

function AddObjectToScene(scene, object, rotation = null) {
	if (rotation) {
		object.rotation.y = rotation;
	}
	scene.add(object);
}

function generateWalls(scene) {
	const orientation = Math.PI / 2;
	AddObjectToScene(scene, topWall, orientation);
	AddObjectToScene(scene, bottomWall, orientation);
	AddObjectToScene(scene, leftWall);
	AddObjectToScene(scene, rightWall);
}

function generateScene(scene) {
	if (maxPlayers == 4) {
		const orientation = Math.PI / 2;
		AddObjectToScene(scene, topPaddle, orientation);
		AddObjectToScene(scene, bottomPaddle, orientation);
	}
	AddObjectToScene(scene, leftPaddle);
	AddObjectToScene(scene, rightPaddle);
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

// Camera Rotation: rendu3d.js:318:13
// X: -56.98787474114721 rendu3d.js:319:13
// Y: -0.09711639542445165 rendu3d.js:320:13
// Z: -0.14947646093265465 rendu3d.js:321:13
// Object { x: 4.337915334242398, y: 14.944152324169096, z: 14.401552868816939 }
// ​
// x: 4.337915334242398
// // ​
// y: 14.944152324169096
// // ​
// z: 14.401552868816939

function setupLight(scene) {
	scene.background = new THREE.Color(background);
	directionalLight.position.set(5, 5, 5);
	directionalLight.castShadow = true;
	axesHelper.position.y = 0;
	AddObjectToScene(scene, ambientLight);
	AddObjectToScene(scene, directionalLight);
	AddObjectToScene(scene, axesHelper);
	// final camera position for 3d view
	scene.add(pivot);
	// Attach the camera to the pivot point
	pivot.add(camera);
	//camera.position.set(-10, 15, 6);
	camera.position.set(4.337915334242398, 14.944152324169096, 14.401552868816939);
	// Rotate the camera
	//rotateCamera(degreesToRadians(214));
	//pivot.rotation.x += degreesToRadians(25);
	//top viuew for debugging
	//camera.position.set(5, 10, 5);
	//camera.lookAt(5, 4, 5);
	camera.lookAt(centerField, 0, centerField);
}

function animate() {
	requestAnimationFrame(animate);
	ballMovement(ball);
	sphere.position.set(ball.x, floatEffect, ball.y);
	leftPaddle.position.z = p1.y;
	rightPaddle.position.z = p2.y;
	if (maxPlayers == 4) {
		topPaddle.position.x = p3.x;
		bottomPaddle.position.x = p4.x;
	}
	renderer.render(scene, camera);
}

function TwoPlayerMovement(key) {
	const upBound = p3StartY - distance + paddleHeight / 2;
	const downBound = p4StartY;
	if (key === "ArrowUp" && p2.y > upBound) p2.y -= speed;
	else if (key === "ArrowDown" && p2.y < downBound) p2.y += speed;
	else if (key === "w" && p1.y > upBound) p1.y -= speed;
	else if (key === "s" && p1.y < downBound) p1.y += speed;
}

function FourPlayerMovement(key) {
	const upOrLeftbound = paddleHeight / 2;
	const downOrRightbound = p2StartX - paddleHeight / 2;
	if (key === "ArrowUp" && p2.y > upOrLeftbound) p2.y -= speed;
	else if (key === "ArrowDown" && p2.y < downOrRightbound) p2.y += speed;
	else if (key === "w" && p1.y > upOrLeftbound) p1.y -= speed;
	else if (key === "s" && p1.y < downOrRightbound) p1.y += speed;
	else if (key === "ArrowLeft" && p3.x > upOrLeftbound) p3.x -= speed;
	else if (key === "ArrowRight" && p3.x < downOrRightbound) p3.x += speed;
	else if (key === "a" && p4.x > upOrLeftbound) p4.x -= speed;
	else if (key === "d" && p4.x < downOrRightbound) p4.x += speed;
}

function radiansToDegrees(radians) {
    return radians * (180 / Math.PI);
}

function printCameraRotationInDegrees(camera) {
    console.log('Camera Rotation:');
    console.log('X:', radiansToDegrees(camera.rotation.x));
    console.log('Y:', radiansToDegrees(camera.rotation.y));
    console.log('Z:', radiansToDegrees(camera.rotation.z));
}

function gameLoop() {
	setupScene();
	setupLight(scene);
	generateScene(scene);
	document.addEventListener("keydown", (event) => {
		if (maxPlayers == 4)
			FourPlayerMovement(event.key);
		else
			TwoPlayerMovement(event.key);
		if (event.key === "r")
			console.log(camera.position, printCameraRotationInDegrees(camera), camera.lookAt);
	});
	animate();
	// const controls = new THREE.OrbitControls(camera, renderer.domElement);
	// controls.enableDamping = true;
	// controls.dampingFactor = 0.05;
	window.addEventListener('resize', () => {
		camera.aspect = container.clientWidth / container.clientHeight;
		camera.updateProjectionMatrix();
		renderer.setSize(container.clientWidth, container.clientHeight);
	});
}

document.addEventListener('DOMContentLoaded', gameLoop);