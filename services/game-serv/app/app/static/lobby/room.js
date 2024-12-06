function getRoomName() {
    let url =  window.location.pathname.split("/");
    return url[2];
}
function getRenderParam() {
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
let render = getRenderParam()
function main() {
    let lobbySocket = new WebSocket(`wss://${window.location.host}/ws/lobby/${getRoomName()}/`);
    lobbySocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data.type == 'lobby_game')
            refresh(data);
        else if (data.type == 'lobby_redirect')
        {
            param = new URLSearchParams(window.location.search);
            param.set("render", render);
            loadPage(`/game/${getRoomName()}/?${param.toString()}`);
        }
    };
    lobbySocket.onclose = function (e) {
        console.error('Lobby socket closed unexpectedly :(');
    };
}

main();

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

function refresh(data) {
    document.getElementById('userCount').textContent = `${data.players.length}/${data.maxPlayers}`;
    playersList = document.getElementById('playersList');
    playersList.innerHTML = '';
    data.players.forEach((player) => addPlayerToList(player, playersList));
    if (data.players.length == data.maxPlayers)
        document.getElementById('launchButton').disabled = false;
    else {
        const newDiv = document.createElement("div");
        newDiv.setAttribute("id", "error-msg");
        newDiv.setAttribute("class", "mt-3");
        newDiv.innerHTML = "<p>Waiting for more players</p>";
        document.getElementById('main').append(newDiv);

        document.getElementById('launchButton').disabled = true;
    }

}

function handlePlayerCount() {
    const status = document.getElementById('2player');
    const currentURL = new URL(window.location.href);
    if (status.checked)
        currentURL.searchParams.append('maxPlayers', '2');
    else
        currentURL.searchParams.append('maxPlayers', '4');
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

function handleRender() {
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

function launchGame() {
    postData(`/lobby/${getRoomName()}/start`)
}