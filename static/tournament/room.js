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

function tournament_refresh(data) {
    document.getElementById('userCount').textContent = `${data.players.length}`;
    playersList = document.getElementById('playersList');
    playersList.innerHTML = '';
    data.players.forEach((player) => addPlayerToList(player, playersList));
    if (data.players.length >= 3)
        document.getElementById('launchButton').disabled = false;
    else {
        document.getElementById('launchButton').disabled = true;
    }

}



function addPlayerToList(playerId, ul) {
    if (playerId == null)
        return;
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

function tournament_launchGame() {
    postData(`/tournament/${document.querySelector('[name=tournamentId]').value}/start`)
}

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
addMain(chat_main);