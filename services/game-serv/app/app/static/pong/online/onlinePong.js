let gameWebSocket;


function clearPopup() {
    let types = ["typeVictory", "typeDefeat", "typeWait", "typeCrash", "messageWon"];
    let content;

    for (let i = 0; i < types.length; i++) {
        content = document.getElementById(types[i]);
        content.style.display = "none";
    }
    content = document.getElementById("message");
    content.innerHTML = '';
    content = document.getElementById("playersList");
    content.innerHTML = '';
    console.log("Clear Popup")
}

function waitPopup() {
    let modal = document.getElementById("modal");
    let popupType = document.getElementById("typeWait");
    let popupMsg = document.getElementById("message");
    let ul = document.getElementById("playersList");

    clearPopup();
    modal.style.display = "flex";
    popupType.style.display = "flex";
    popupMsg.innerHTML = "<div id=\"timer\" style=\"display: inline;\"></div>s";
    ul.innerHTML = '';
    console.log("wait popup")
}

function endPopup(typeStr, winner) {
    let modal = document.getElementById("modal");
    let msg = document.getElementById("messageWon");
    let player = document.getElementById("playersList");
    let type = document.getElementById(typeStr);

    clearPopup();
    modal.style.display = "flex";
    type.style.display = "flex";
    msg.style.display = "flex";
    player.innerHTML = '';
    addPlayerToList(winner, player);
    console.log("end popup")
}

function crashPopup() {
    let modal = document.getElementById("modal");
    let popupType = document.getElementById("typeCrash");

    clearPopup();
    modal.style.display = "flex";
    popupType.style.display = "flex";
    console.log("crash popup")
}

function addPlayerToList(playerId, ul) {
    const element =  fetch("/api/player/" + playerId + "/html/")
    .then(data => {
        return data.text();
    })
    .then(html => {
        li = document.createElement('li')
        li.innerHTML = html
        ul.appendChild(li)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
    
async function sendMove(gameWebSocket) {
    if (paddleMove != 0) {
        gameWebSocket.send(JSON.stringify({ "type": "move", "paddleMove": paddleMove }))
        paddleMove = 0
    }
}

async function startAnimation() {
    disableDoubleTapZoom();
    blockContextMenu();
    hideNavbar();

    let One = document.getElementById("1");
    let Two = document.getElementById("2");
    let Three = document.getElementById("3");
    let SVGBall = document.getElementById("ball");
    SVGBall.style.display = "none";
    Three.style.display = "block";
    await sleep(1000);
    Three.style.display = "none";
    Two.style.display = "block";
    await sleep(1000);
    Two.style.display = "none";
    One.style.display = "block";
    await sleep(1000);
    One.style.display = "none";
    SVGBall.style.display = "block";
}

