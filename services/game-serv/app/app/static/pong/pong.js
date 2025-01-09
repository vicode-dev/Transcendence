class Ball {
	constructor(x, y, angle) {
		this.x = x;
		this.y = y;
		this.angle = angle;
		this.speed = INIT_SPEED;
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
const INIT_SPEED = 2;

let ball;
let p1;
let p2;
let p3;
let p4;
let paddleMove;
let loopBreaker;
let error;

let timers = {};

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

function resetAngle(idx, score) {
    let angles = [180, 0, 270, 90];
    let j;

    for (let i = idx; i < idx + 4; i++) {
        j = i % 4;
        if (j != idx && score[j] > 0)
            return angles[j];
    }
    return 0;
}

function ballHitPlayer(ball, startAngle, diff, ballPos) {
    ball.angle = (360 + startAngle + (diff / (PADDLE_SIZE + 2 * BALL_SIZE)) * (ballPos + BALL_SIZE)) % 360
}


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function drawBall() {
    let SVGBall = document.getElementById("ball");
    SVGBall.style.transition = '';
    SVGBall.style.transform = `translate(${ball.x}px, ${ball.y}px)`;
}

function resetClick(buttonId) {
    if (timers[buttonId]) {
        clearInterval(timers[buttonId]);
        delete timers[buttonId];
    }
}

function movePaddle(move, buttonId) {
    resetClick(buttonId);
    timers[buttonId] = setInterval(function() {
        paddleMove = move;
    }, 50);
}

function blockContextMenu() {
    window.oncontextmenu = function(event) {
        if (event.button !== 2) {
            event.preventDefault();
        }
    };
}

function listenForScreenChange() {
    function onFullscreenChange() {
        if (!document.fullscreenElement) {
            document.getElementById("nav").style.display = "block";
            document.getElementById("enterFullScreen").style.display = "block";
            document.getElementById("exitFullScreen").style.display = "none";
            document.removeEventListener("fullscreenchange", onFullscreenChange);
        }
    }
    function onWebkitFullscreenChange() {
        if (!document.webkitFullscreenElement) {
            document.getElementById("nav").style.display = "block";
            document.getElementById("enterFullScreen").style.display = "block";
            document.getElementById("exitFullScreen").style.display = "none";
            document.removeEventListener("webkitfullscreenchange", onWebkitFullscreenChange);
        }
    }
    function onMSFullscreenChange() {
        if (!document.msFullscreenElement) {
            document.getElementById("nav").style.display = "block";
            document.getElementById("enterFullScreen").style.display = "block";
            document.getElementById("exitFullScreen").style.display = "none";
            document.removeEventListener("MSFullscreenChange", onMSFullscreenChange);
        }
    }
    document.addEventListener("fullscreenchange", onFullscreenChange);
    document.addEventListener("webkitfullscreenchange", onWebkitFullscreenChange);
    document.addEventListener("MSFullscreenChange", onMSFullscreenChange);
}

function enterFullScreen() {
    if(screen.width <= 400) {
        try {
            if (!document.fullscreenElement) {
                if (document.documentElement.requestFullscreen) {
                    document.documentElement.requestFullscreen();
                } else if (document.documentElement.webkitRequestFullscreen) {
                    document.documentElement.webkitRequestFullscreen();
                } else if (document.documentElement.webkitEnterFullscreen) {
                    document.documentElement.webkitEnterFullscreen();
                } else if (document.documentElement.msRequestFullscreen) {
                    document.documentElement.msRequestFullscreen();
                }
                document.getElementById("nav").style.display = "none";
                document.getElementById("enterFullScreen").style.display = "none";
                document.getElementById("exitFullScreen").style.display = "block";
            } else {
                if (document.documentElement.exitFullscreen) {
                    document.documentElement.exitFullscreen();
                } else if (document.documentElement.webkitExitFullscreen) {
                    document.documentElement.webkitExitFullscreen();
                } else if (window.document.documentElement.msExitFullscreen) {
                    document.documentElement.msExitFullscreen();
                }
                // document.getElementById("enterFullScreen").style.display = "block";
            }
        } catch (error) {
            window.alert("Error full screen");
        }
    }
    listenForScreenChange();
}

function exitFullScreen() {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) {
        document.msExitFullscreen();
    }
    document.getElementById("nav").style.display = "block";
    showNavbar();
    document.getElementById("exitFullScreen").style.display = "none";
    document.getElementById("enterFullScreen").style.display = "block";
}    

function disableDoubleTapZoom() {
    let lastTouchTime = 0;

    document.addEventListener('touchend', (event) => {
        const now = Date.now();
        if (now - lastTouchTime <= 300) {
            event.preventDefault(); // Prevent double-tap zoom
        }
        lastTouchTime = now;
    }, { passive: false });    
}

function showNavbar() {
    document.getElementById("nav").style.bottom = "0";
}

function hideNavbar() {
    document.getElementById("nav").style.bottom = "-100px";
}