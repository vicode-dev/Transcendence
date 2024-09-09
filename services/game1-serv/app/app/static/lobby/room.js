const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const lobbySocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/lobby/'
    + roomName
    + '/'
);

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        mode: 'same-origin',
        body: JSON.stringify(data)
    });
    
    if (!response.ok)
        throw new Error('Network response was not ok');
    return response.json();
}

function refresh(data)
{
    document.getElementById('userCount').textContent = 
    data.players.length
    + '/'
    +  data.maxnumber + '\n';
    const ul = document.getElementById('playersList')
    ul.innerHTML = ''
    data.players.forEach(function(player)
    {
        li = document.createElement('li')
        li.textContent = player
        ul.appendChild(li)
    })
    if (data.players.length == data.maxnumber)
        document.getElementById('launchButton').disabled = false
    else
        document.getElementById('launchButton').disabled = true

}

function launchGame()
{
    postData('/lobby/api/start', {room_name: roomName})
    .then(console.log('ok'))
    .catch(error => {
        console.error('Error:', error);
    });
}

lobbySocket.onmessage = function(e)
{
    const data = JSON.parse(e.data);
    console.log(data);
    if (data.type == 'lobby_game')
        refresh(data)
    else if (data.type == 'lobby_redirect')
        window.location.href = '/game/' + roomName
};

lobbySocket.onclose = function(e)
{
    console.error('Lobby socket closed unexpectedly');
};