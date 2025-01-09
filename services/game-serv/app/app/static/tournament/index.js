async function createTournament(event) {
    response = await fetch(`/tournament/api/create`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        mode: 'same-origin',
    })
    if (response.status == 200) {
        content = await response.json();
        room_url = `/tournament/${content.id}/`;
        loadPageEvent(event, room_url);
    } else {
        content = await response.text();
        console.error('Error:', content);
    };
}

function join(event) {
    id = document.getElementById('tournamentId').value
    room_url = `/tournament/${id}`;
    loadPageEvent(event, room_url);
}
