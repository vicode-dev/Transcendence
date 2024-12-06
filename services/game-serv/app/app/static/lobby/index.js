// const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

async function postData(url = '', data = {}) {
const response = await fetch(url, {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
    },
    mode: 'same-origin',
});

if (!response.ok)
    throw new Error('Network response was not ok');
return response.json();
}

function create(event) {
    let nbPlayer = document.querySelector('input[type=radio][name=players]:checked').value;
    let gameType = document.querySelector('input[type=radio][name=gameType]:checked').value;
	let searchParams = new URLSearchParams();
	searchParams.set("maxPlayers", nbPlayer);
	searchParams.set("gameType", gameType);
    postData(`/lobby/api/create/?${searchParams.toString()}`)
    .then(data => {
        console.log('Success:', data);
        room_url = `/lobby/${data.id}/`;
        loadPageEvent(event, room_url);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function join(event) {
    id = document.getElementById('lobbyId').value
    // window.location.href = "/lobby/" + id
    room_url = "/lobby/" + id;
    loadPageEvent(event, room_url);
}