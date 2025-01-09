function copy_text(button_id = false)

{
    const copy_text = window.location.href;


        if (navigator.clipboard)
        {
            navigator.clipboard.writeText(copy_text);
            if (button_id)
            {
                const button = document.getElementById(button_id);
                if (button)
                {
                    button.innerHTML = '<i class="fa-solid fa-copy"></i>';
                    setTimeout(() => {
                        button.innerHTML = '<i class="fa-regular fa-copy"></i>';
                    }, 400);
                }
            }
        }
}

function lobby_getRenderParam() {
    let params = new URLSearchParams(document.location.search);
    let render = parseInt(params.get("render"), 2);
    if(render)
    {
        document.getElementById("render").checked = true;
        return(true)
    }
    else
        return(false)
}

let render
let lobbySocket

async function postData(url = '') {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
    });
    
    if (!response.ok)
    console.error('Error:', response.status);
}

function lobby_refresh(data) {
    document.getElementById('userCount').textContent = `${data.players.length}/${data.maxPlayers}`;
    playersList = document.getElementById('playersList');
    playersList.innerHTML = '';
    data.players.forEach((player) => addPlayerToList(player, playersList));
    if (data.players.length == data.maxPlayers)
    document.getElementById('launchButton').disabled = false;
    else {
        // const newDiv = document.createElement("div");
        // newDiv.setAttribute("id", "error-msg");
        // newDiv.setAttribute("class", "mt-3");
        // newDiv.innerHTML = "<p>Waiting for more players</p>";
        // document.getElementById('main').append(newDiv);
        
        document.getElementById('launchButton').disabled = true;
    }
    
}

function handlePlayerCount() {
    const status = document.getElementById('playercount');
    const currentURL = new URL(window.location.href);
    if (status.checked)
    currentURL.searchParams.append('maxPlayers', '4');
    else
    currentURL.searchParams.append('maxPlayers', '2');
    postData(currentURL.href)
}

function handleVisibility() {
    const status = document.getElementById('private');
    const currentURL = new URL(window.location.href);
    if (status.checked)
    currentURL.searchParams.append('private', '1');
    else
    currentURL.searchParams.append('private', '0');
    postData(currentURL.href)
}

function lobby_handleRender() {
    let status = document.getElementById('render').checked;
    render = status
}

function addPlayerToList(playerId, ul) {
    fetch("/api/player/" + playerId + "/html/")
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

function lobby_launchGame() {
    postData(`/lobby/${document.querySelector('[name=roomId]').value}/start`)
}

function lobby_mainRoom() {
    render = lobby_getRenderParam();
    lobbySocket = new WebSocket(`wss://${window.location.host}/ws/lobby/${document.querySelector('[name=roomId]').value}/`);
    destructors.push(lobby_destructorRoom);
    lobbySocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data.type == 'lobby_game')
            lobby_refresh(data);
        else if (data.type == 'lobby_redirect')
        {
            param = new URLSearchParams(window.location.search);
            
            param.set("render", render);
            loadPage(`/game/${document.querySelector('[name=roomId]').value}/?${param.toString()}`).then();
        }
    };
    lobbySocket.onclose = function (e) {
        if (e.wasClean == false)
        console.error('Chat socket crashed', e);    };
}

function lobby_destructorRoom() {
    lobbySocket.close();
    lobbySocket = null;
}

addMain(lobby_mainRoom);