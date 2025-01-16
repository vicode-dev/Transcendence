function hidePong () {
    document.getElementById('pong-content').style.display ='none';
    let pongRequiredInputs = document.getElementsByClassName('pong-required');
    for (const pongRequiredInput of pongRequiredInputs) {
        pongRequiredInput.removeAttribute("required");
    }
}

function showPong () {
    document.getElementById('pong-content').style.display ='block';
    pongRequiredInputs = document.getElementsByClassName('pong-required');
    for (pongRequiredInput of pongRequiredInputs) {
        pongRequiredInput.setAttribute("required", "");
    }
}

function showRender () {
    // document.getElementById('online-content').style.display = 'block';
    // pongRequiredInputs = document.getElementsByClassName('online-required');
    // for (pongRequiredInput of pongRequiredInputs) {
    //     pongRequiredInput.setAttribute("required", "");
    // }
}

function hideRender () {
    // document.getElementById('online-content').style.display = 'none';
    // pongRequiredInputs = document.getElementsByClassName('online-required');
    // for (pongRequiredInput of pongRequiredInputs) {
    //     pongRequiredInput.removeAttribute("required", "");
    // }
}

async function matchmaking(gameType, maxPlayers, render) {
    let searchParams = new URLSearchParams();
    searchParams.set("gameType", gameType);

    console.log("gameType, maxPlayers, Render: ", gameType, maxPlayers, render);

    if (gameType === "false") { //Pong
        searchParams.set("maxPlayers", maxPlayers);
    }
    const response = await fetch(`/game/api/join/?${searchParams.toString()}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
    })
    if (response.status == 200) {
        const data = await response.json();
        if (render === "true")
            loadPage(`/lobby/${data.gameId}/?render=` + render );
        else
            loadPage(`/lobby/${data.gameId}/`);
    } else {
        const errorData = await response.text();
        console.error('Error:', errorData);
    }
    return;
}

function loadLocalGame(event, localgameUrl) {
    let render = 0;
    let maxPlayers = 0;

    event.preventDefault();
    const url = new URL(localgameUrl, window.location.href);

    const gameType = document.querySelector('input[type=radio][name=gameType]:checked').value;
    url.searchParams.append('gameType', gameType);
    if (gameType === "false") //Pong
    {
        maxPlayers = document.querySelector('input[type=radio][name=maxPlayers]:checked').value;
        if (document.querySelector('input[type=radio][name=render]:checked'))
        {
            render = document.querySelector('input[type=radio][name=render]:checked').value;
        }
        url.searchParams.append('maxPlayers', maxPlayers);
        url.searchParams.append('render', render);        
    }
    if (document.querySelector('input[type=radio][name=matchmaking]:checked').value == 'online')
        return matchmaking(gameType, maxPlayers, render);

    document.getElementById('pong-content').style.display ='none';
    loadPageEvent(event, url.toString());
}

// function gameSelectMain() {
    // document.getElementById('pong-content').style.display ='none';
    // const   formButton = document.getElementById('submit-form');
    // formButton.style.display = "none";

    // document.getElementById('game-form').addEventListener('input', function() {
    //     const   isFormValid = document.getElementById('game-form').checkValidity();
    //     if (isFormValid)
    //     {
    //         formButton.style.display = "block";
    //     }
    // })
// }

// addMain(gameSelectMain);