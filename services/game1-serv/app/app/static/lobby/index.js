const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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

function create() {
var nbPlayer = document.querySelector('input[type=radio][name=players]:checked').value;
postData('/lobby/api/create', { maxplayer: nbPlayer })
.then(data => {
    let Game = JSON.parse(data)
    console.log('Success:', Game);
    window.location.href = "/lobby/" + Game[0].pk
})
.catch(error => {
    console.error('Error:', error);
});
}

function join() {
        id = document.getElementById('lobbyId').value
        window.location.href = "/lobby/" + id
}