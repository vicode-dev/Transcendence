// function showPlayersFields() {
//     document.getElementById('players-fields').style.display = 'block';
// }

// function hidePlayersFields() {
//     document.getElementById('players-fields').style.display = 'none';
// }

async function create(event) {
    // let nbPlayer = document.querySelector('input[type=radio][name=players]:checked').value;
    let gameType = document.querySelector('input[type=radio][name=gameType]:checked').value;
    let searchParams = new URLSearchParams();
    // searchParams.set("maxPlayers", nbPlayer);
    searchParams.set("gameType", gameType);
    response = await fetch(`/lobby/api/create/?${searchParams.toString()}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        mode: 'same-origin',
    })
    if (response.status == 200) {
        content = await response.json();
        console.log('Success:', content);
        room_url = `/lobby/${content.id}/`;
        loadPageEvent(event, room_url);
    } else {
        content = await response.text();
        console.error('Error:', content);
    };
}

function join(event) {
    id = document.getElementById('lobbyId').value
    room_url = "/lobby/" + id;
    loadPageEvent(event, room_url);
}