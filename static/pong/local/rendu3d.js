// /* GLobal constants*/
// const centerField = 4.5;
// const floatEffect = 0.5;
// const paddleHeight = 1.5;
// const paddleWidth = 0.25;
// const paddleDepth = 0.2;
// const p1StartX = 0;
// const p1StartY = centerField;
// const p2StartX = 8.75;
// const p2StartY = centerField;
// const p3StartX = centerField;
// const p3StartY = 0;
// const p4StartX = centerField;
// const p4StartY = 8.75;
// // const yellow = 0xffff00;
// // const pink = 0xe070d0;
// // const white = 0xffffff;
// //const background = 0x2d3247;
// const root = document.documentElement;
// const style = getComputedStyle(root);
// const background = style.getPropertyValue('--background-color').trim(); // Retrieve the CSS variable
// const white = style.getPropertyValue('--secondary-color').trim(); // Retrieve the CSS variable
// const yellow = style.getPropertyValue('--accent-color').trim(); // Retrieve the CSS variable
// const pink = style.getPropertyValue('--secondary-color').trim(); // Retrieve the CSS variable
// const radius = 0.125;
// const heightSegments = 32;
// const widthSegments = heightSegments;
// const wallHeight = 0.5;
// const wallDepth = paddleWidth;
// const wallLength = 10.75;
// const speed = 0.25;
// const distance = 1;
// const scene = new THREE.Scene();
// const renderer = new THREE.WebGLRenderer({ antialias: true });
// const container = document.getElementById('center-div');
// const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
// const ambientLight = new THREE.AmbientLight(white, 0.6);
// const directionalLight = new THREE.DirectionalLight(white, 0.8);
// const maxPlayers = container.dataset.maxPlayers;
// const axesHelper = new THREE.AxesHelper(5); // The argument is the size of the axes
// const sensitivity = 130;

// // --- Game Logic Classes ---
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

// function createBoxGeometry({ position, size, color = 0xffffff } = {}) {
// 	const geometry = new THREE.BoxGeometry(size.x, size.y, size.z);
// 	const material = new THREE.MeshBasicMaterial({ color });
// 	const box = new THREE.Mesh(geometry, material);
// 	box.position.copy(position);
// 	return box;
// }

// function createPaddle({ position, color = 0xffffff } = {}) {
// 	return createBoxGeometry({ position, size: new THREE.Vector3(paddleWidth, paddleDepth, paddleHeight), color });
// }

// function createWall({ position }) {
// 	return createBoxGeometry({ position, size: new THREE.Vector3(wallDepth, wallHeight, wallLength), white });
// }

// function createBall({ position, radius, color = 0xffffff } = {}) {
// 	const geometry = new THREE.SphereGeometry(radius, widthSegments, heightSegments);
// 	const material = new THREE.MeshStandardMaterial({ color });
// 	const ball = new THREE.Mesh(geometry, material);
// 	ball.position.copy(position);
// 	return ball;
// }

// /* Players*/
// const p1 = new Player(p1StartX, p1StartY);
// const leftPaddle = createPaddle({
// 	position: new THREE.Vector3(p1StartX, floatEffect, p1StartY),
// 	color: yellow
// });

// const p2 = new Player(p2StartX, p2StartY);
// const rightPaddle = createPaddle({
// 	position: new THREE.Vector3(p2StartX, floatEffect, p2StartY),
// 	color: yellow
// })

// const p3 = new Player(p3StartX, p3StartY);
// const topPaddle = createPaddle({
// 	position: new THREE.Vector3(p3StartX, floatEffect, p3StartY),
// 	color: yellow
// })

// const p4 = new Player(p4StartX, p4StartY);
// const bottomPaddle = createPaddle({
// 	position: new THREE.Vector3(p4StartX, floatEffect, p4StartY),
// 	color: yellow
// })

// /* Ball*/
// const ball = new Ball(centerField, centerField, Math.PI);
// const sphere = createBall({
// 	position: new THREE.Vector3(centerField, floatEffect, centerField),
// 	radius: radius,
// 	color: pink
// })

// /* Walls */
// const leftWall = createWall({ position: new THREE.Vector3(p1StartX - distance, wallHeight, centerField) })
// const rightWall = createWall({ position: new THREE.Vector3(p2StartX + distance, wallHeight, centerField) })
// const topWall = createWall({ position: new THREE.Vector3(centerField, wallHeight, p3StartY - distance) })
// const bottomWall = createWall({ position: new THREE.Vector3(centerField, wallHeight, p4StartY + distance) })

// // --- Game Logic Math ---
// function resetBall(ball, angle) {
// 	// Calculate the ball's new position
// 	ball.speed = 0.1; // Reset ball speed
// 	ball.x = centerField;
// 	ball.y = centerField;
// 	ball.angle = angle;
// }

// function degreesToRadians(angle) {
// 	return angle * (Math.PI / 180);
// }

// function isBallHittingPaddle(ballMesh, paddleMesh) {
// 	const ballWorldPosition = new THREE.Vector3();
// 	ballMesh.getWorldPosition(ballWorldPosition);

// 	const ballRadius = ballMesh.geometry.parameters.radius * ballMesh.scale.x; // Account for scaling
// 	const ballBoundingSphere = new THREE.Sphere(ballWorldPosition, ballRadius);
// 	const paddleBoundingBox = new THREE.Box3().setFromObject(paddleMesh);

// 	// Check if the ball intersects with the paddle
// 	const isHitting = paddleBoundingBox.intersectsSphere(ballBoundingSphere);
// 	if (isHitting) {
// 		// Calculate the relative hit position (-1 is left/top, 0 is center, +1 is right/bottom)
// 		const paddleCenter = paddleMesh.position.clone();
// 		let relativeHitPosition = (ballWorldPosition.z - paddleCenter.z) / (paddleHeight / 2); // For vertical paddles
// 		// Invert the relative hit position for the right paddle
// 		if (paddleMesh.position.x > 0) { // Assuming right paddle has positive x position
// 			relativeHitPosition = -relativeHitPosition;
// 		}

// 		return { isHitting: true, relativeHitPosition: THREE.MathUtils.clamp(relativeHitPosition, -1, 1) };
// 	}
// 	return { isHitting: false, relativeHitPosition: 0 };
// }

// function playerCollision(sphere, paddle) {
// 	const collision = isBallHittingPaddle(sphere, paddle);
// 	if (collision.isHitting) {
// 		// Reflect ball's angle based on hit position
// 		const relativeHitPosition = collision.relativeHitPosition;
// 		// Change the ball's angle based on how far from the center it hit (steeper bounce for edges)
// 		ball.angle = 180 + ball.angle + relativeHitPosition * sensitivity;
// 		return true;
// 	}
// 	return false;
// }


// function wallCollision(sphere) {
// 	if (isBallHittingPaddle(sphere, leftWall).isHitting)
// 		resetBall(ball, 0);
// 	else if (isBallHittingPaddle(sphere, rightWall).isHitting)
// 		resetBall(ball, 180);
// 	else if (maxPlayers == 4 && isBallHittingPaddle(sphere, topWall).isHitting)
// 		resetBall(ball, 90);
// 	else if (maxPlayers == 4 && isBallHittingPaddle(sphere, bottomWall).isHitting)
// 		resetBall(ball, 270);
// 	else {
// 		if (isBallHittingPaddle(sphere, topWall).isHitting)
// 			ball.y = ball.y + wallDepth;
// 		else if (isBallHittingPaddle(sphere, bottomWall).isHitting)
// 			ball.y = ball.y - wallDepth;
// 		else
// 			return false;
// 		ball.angle = -ball.angle;
// 	}
// 	return true;
// }

// function ballMovement(ball) {
// 	// Check for player collisions
// 	if (playerCollision(sphere, leftPaddle)) {
// 		ball.x = paddleWidth;
// 	}
// 	if (playerCollision(sphere, rightPaddle)) {
// 		ball.x = p2StartX - paddleWidth;
// 	}
// 	if (maxPlayers == 4) {
// 		if (playerCollision(sphere, topPaddle)) {
// 			ball.y = paddleWidth;
// 		}
// 		if (playerCollision(sphere, bottomPaddle)) {
// 			ball.y = p4StartY - paddleWidth;
// 		}
// 	}

// 	// Calculate the ball's new position
// 	let y = ball.y + Math.sin(degreesToRadians(ball.angle)) * ball.speed;
// 	let x = ball.x + Math.cos(degreesToRadians(ball.angle)) * ball.speed;
// 	// Check for wall collisions
// 	if (!wallCollision(sphere)) {
// 		ball.x = x;
// 		ball.y = y;
// 	}
// }

// function AddObjectToScene(scene, object, rotation = null) {
// 	if (rotation) {
// 		object.rotation.y = rotation;
// 	}
// 	scene.add(object);
// }

// function generateWalls(scene) {
// 	const orientation = Math.PI / 2;
// 	AddObjectToScene(scene, topWall, orientation);
// 	AddObjectToScene(scene, bottomWall, orientation);
// 	AddObjectToScene(scene, leftWall);
// 	AddObjectToScene(scene, rightWall);
// }

// function generateScene(scene) {
// 	if (maxPlayers == 4) {
// 		const orientation = Math.PI / 2;
// 		AddObjectToScene(scene, topPaddle, orientation);
// 		AddObjectToScene(scene, bottomPaddle, orientation);
// 	}
// 	AddObjectToScene(scene, leftPaddle);
// 	AddObjectToScene(scene, rightPaddle);
// 	AddObjectToScene(scene, sphere);
// 	generateWalls(scene);
// }

// function setupScene() {
// 	renderer.setSize(container.clientWidth, container.clientHeight);
// 	renderer.shadowMap.enabled = true;
// 	container.appendChild(renderer.domElement);
// }

// const pivot = new THREE.Object3D();
// function rotateCamera() {
// 	pivot.rotation.y = degreesToRadians(-0.09711639542445165);
// 	pivot.rotation.x = degreesToRadians(-56.98787474114721);
// 	pivot.rotation.z = degreesToRadians(-0.14947646093265465);
// 	//pivot.rotation.x += angle;
// }

// // Camera Rotation: rendu3d.js:318:13
// // X: -56.98787474114721 rendu3d.js:319:13
// // Y: -0.09711639542445165 rendu3d.js:320:13
// // Z: -0.14947646093265465 rendu3d.js:321:13
// // Object { x: 4.337915334242398, y: 14.944152324169096, z: 14.401552868816939 }
// // ​
// // x: 4.337915334242398
// // // ​
// // y: 14.944152324169096
// // // ​
// // z: 14.401552868816939

// function setupLight(scene) {
// 	scene.background = new THREE.Color(background);
// 	directionalLight.position.set(5, 5, 5);
// 	directionalLight.castShadow = true;
// 	axesHelper.position.y = 0;
// 	AddObjectToScene(scene, ambientLight);
// 	AddObjectToScene(scene, directionalLight);
// 	AddObjectToScene(scene, axesHelper);
// 	// final camera position for 3d view
// 	scene.add(pivot);
// 	// Attach the camera to the pivot point
// 	pivot.add(camera);
// 	//camera.position.set(-10, 15, 6);
// 	camera.position.set(4.337915334242398, 14.944152324169096, 14.401552868816939);
// 	// Rotate the camera
// 	//rotateCamera(degreesToRadians(214));
// 	//pivot.rotation.x += degreesToRadians(25);
// 	//top viuew for debugging
// 	//camera.position.set(5, 10, 5);
// 	//camera.lookAt(5, 4, 5);
// 	camera.lookAt(centerField, 0, centerField);
// }

// function animate() {
// 	requestAnimationFrame(animate);
// 	ballMovement(ball);
// 	sphere.position.set(ball.x, floatEffect, ball.y);
// 	leftPaddle.position.z = p1.y;
// 	rightPaddle.position.z = p2.y;
// 	if (maxPlayers == 4) {
// 		topPaddle.position.x = p3.x;
// 		bottomPaddle.position.x = p4.x;
// 	}
// 	renderer.render(scene, camera);
// }

// function TwoPlayerMovement(key) {
// 	const upBound = p3StartY - distance + paddleHeight / 2;
// 	const downBound = p4StartY;
// 	if (key === "ArrowUp" && p2.y > upBound) p2.y -= speed;
// 	else if (key === "ArrowDown" && p2.y < downBound) p2.y += speed;
// 	else if (key === "w" && p1.y > upBound) p1.y -= speed;
// 	else if (key === "s" && p1.y < downBound) p1.y += speed;
// }

// function FourPlayerMovement(key) {
// 	const upOrLeftbound = paddleHeight / 2;
// 	const downOrRightbound = p2StartX - paddleHeight / 2;
// 	if (key === "ArrowUp" && p2.y > upOrLeftbound) p2.y -= speed;
// 	else if (key === "ArrowDown" && p2.y < downOrRightbound) p2.y += speed;
// 	else if (key === "w" && p1.y > upOrLeftbound) p1.y -= speed;
// 	else if (key === "s" && p1.y < downOrRightbound) p1.y += speed;
// 	else if (key === "ArrowLeft" && p3.x > upOrLeftbound) p3.x -= speed;
// 	else if (key === "ArrowRight" && p3.x < downOrRightbound) p3.x += speed;
// 	else if (key === "a" && p4.x > upOrLeftbound) p4.x -= speed;
// 	else if (key === "d" && p4.x < downOrRightbound) p4.x += speed;
// }

// function radiansToDegrees(radians) {
//     return radians * (180 / Math.PI);
// }

// function printCameraRotationInDegrees(camera) {
//     console.log('Camera Rotation:');
//     console.log('X:', radiansToDegrees(camera.rotation.x));
//     console.log('Y:', radiansToDegrees(camera.rotation.y));
//     console.log('Z:', radiansToDegrees(camera.rotation.z));
// }

// function gameLoop() {
// 	setupScene();
// 	setupLight(scene);
// 	generateScene(scene);
// 	document.addEventListener("keydown", (event) => {
// 		if (maxPlayers == 4)
// 			FourPlayerMovement(event.key);
// 		else
// 			TwoPlayerMovement(event.key);
// 		if (event.key === "r")
// 			console.log(camera.position, printCameraRotationInDegrees(camera), camera.lookAt);
// 	});
// 	animate();
// 	// const controls = new THREE.OrbitControls(camera, renderer.domElement);
// 	// controls.enableDamping = true;
// 	// controls.dampingFactor = 0.05;
// 	window.addEventListener('resize', () => {
// 		camera.aspect = container.clientWidth / container.clientHeight;
// 		camera.updateProjectionMatrix();
// 		renderer.setSize(container.clientWidth, container.clientHeight);
// 	});
// }

// document.addEventListener('DOMContentLoaded', gameLoop);