// function resetClick(buttonId) {
//     if (timers[buttonId]) {
//         clearInterval(timers[buttonId]);
//         delete timers[buttonId];
//     }
// }

// function clickDown(move, buttonId) {
//     resetClick(buttonId);
//     timers[buttonId] = setInterval(function() {
//         if (move === "w" || move === "s")
//             moveLeftPaddle(move);
//         if (move === "ArrowUp" || move === "ArrowDown")
//             moveRightPaddle(move);
//         if (move === "ArrowLeft" || move === "ArrowRight")
//             moveTopPaddle(move);
//         if (move === "a" || move === "d")
//             moveBottomPaddle(move);
//     }, 50);
// }

function clickDown(move) {
    resetClick(move);
    timers[move] = setInterval(function() {
        if (move === "w" || move === "s")
            moveLeftPaddle(move);
        if (move === "ArrowUp" || move === "ArrowDown")
            moveRightPaddle(move);
        if (move === "ArrowLeft" || move === "ArrowRight")
            moveTopPaddle(move);
        if (move === "a" || move === "d")
            moveBottomPaddle(move);
    }, 50);
}

function moveLeftPaddle(move) {
    let leftPaddle = document.getElementById("leftPaddle");
    let wall = 0; 
    if (!leftPaddle || !p1)
        return ;
    if (p3 || p4)
       wall = PADDLE_WIDTH;
    if (move === "w" && p1.y > wall) {
        p1.y -= 0.25;
    } else if (move === "s" && p1.y < SIZE - PADDLE_SIZE - wall) {
        p1.y += 0.25;
    }
    leftPaddle.setAttribute("y", p1.y);
}

function moveRightPaddle(move) {
    let rightPaddle = document.getElementById("rightPaddle");
    let wall = 0;
    if (!rightPaddle || !p2)
        return ;
    if (p3 || p4)
        wall = PADDLE_WIDTH;
    if (move === "ArrowUp" && p2.y > wall) {
        p2.y -= 0.25;
    } else if (move === "ArrowDown" && p2.y < SIZE - PADDLE_SIZE - wall) {
        p2.y += 0.25;
    }
    rightPaddle.setAttribute("y", p2.y);
}

function moveTopPaddle(move) {
    let topPaddle = document.getElementById("topPaddle");
    if (!topPaddle || !p3)
        return ;
    if (move === "ArrowLeft" && p3.x > PADDLE_WIDTH) {
        p3.x -= 0.25;
    } else if (move === "ArrowRight" && p3.x < SIZE - PADDLE_SIZE - PADDLE_WIDTH) {
        p3.x += 0.25;
    }
    topPaddle.setAttribute("x", p3.x);
}

function moveBottomPaddle(move) {
    let bottomPaddle = document.getElementById("bottomPaddle");
    if (!bottomPaddle || !p4)
        return ;
    if (move === "a" && p4.x > PADDLE_WIDTH) {
        p4.x -= 0.25;
    } else if (move === "d" && p4.x < SIZE - PADDLE_SIZE - PADDLE_WIDTH) {
        p4.x += 0.25;
    }
    bottomPaddle.setAttribute("x", p4.x);
}

function initPos() {
    let leftPaddle = document.getElementById("leftPaddle");
    let rightPaddle = document.getElementById("rightPaddle");
    let score1 = document.getElementById("score1");
    let score2 = document.getElementById("score2");

    // document.getElementById("winner-msg").innerText = '';
    leftPaddle.setAttribute("x", 0);
    leftPaddle.setAttribute("y", 3.75);
    rightPaddle.setAttribute("x", 8.75);
    rightPaddle.setAttribute("y", 3.75);
    score1.textContent = 0;
    score2.textContent = 0;
    if (p3 && p4) {
        let topPaddle = document.getElementById("topPaddle");
        let bottomPaddle = document.getElementById("bottomPaddle");
        let score3 = document.getElementById("score3");
        let score4 = document.getElementById("score4");

        topPaddle.setAttribute("x", 3.75);
        topPaddle.setAttribute("y", 0);
        bottomPaddle.setAttribute("x", 3.75);
        bottomPaddle.setAttribute("y", 8.75);
        score1.textContent = 5;
        score2.textContent = 5;
        score3.textContent = 5;
        score4.textContent = 5;
    }
}