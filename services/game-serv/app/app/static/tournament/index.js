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

function createTournament(event) {
    postData('/tournament/api/create')
    .then(data => {
        let tournament = data
        room_url = "/tournament/" + tournament.id;
        loadPageEvent(event, room_url);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function join(event) {
    id = document.getElementById('tournamentId').value
    room_url = "/tournament/" + id;
    loadPageEvent(event, room_url);
}