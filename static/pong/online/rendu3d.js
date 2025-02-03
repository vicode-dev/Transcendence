let root;
let style;
let background; // Retrieve the CSS variable
let white; // Retrieve the CSS variable
let yellow; // Retrieve the CSS variable
let pink;
let scene;
let renderer;
let container;
let camera;
let axesHelper; // The argument is the size of the axes
let ambientLight;
let directionalLight;

let pivot;

let leftWall;
let rightWall;
let topWall;
let bottomWall;

let leftPaddle;
let rightPaddle;
let topPaddle;
let bottomPaddle;
let sphere;

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

function setupScene() {
	renderer.setSize(container.clientWidth, container.clientHeight);
	renderer.shadowMap.enabled = true;
	container.appendChild(renderer.domElement);
}

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
	// axesHelper.position.y = 0;
	AddObjectToScene(scene, ambientLight);
	AddObjectToScene(scene, directionalLight);
	// AddObjectToScene(scene, axesHelper);
	scene.add(pivot);
	pivot.add(camera);
	camera.position.set(4.337915334242398, 14.944152324169096, 14.401552868816939);
	camera.lookAt(SIZE / 2, 0, SIZE / 2);
}

function printCameraRotationInDegrees(camera) {
    console.log('Camera Rotation:');
    console.log('X:', radiansToDegrees(camera.rotation.x));
    console.log('Y:', radiansToDegrees(camera.rotation.y));
    console.log('Z:', radiansToDegrees(camera.rotation.z));
}

