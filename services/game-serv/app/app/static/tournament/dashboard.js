function tournament_main() {
    reconnect();
}

function gameList(data) {
    let gameList = document.getElementById('gameList');
    gameList.innerHTML = '';
    data.games.forEach(game => {
        if (game == "None")
            return;
        fetch('/game/' + game + '/api').then(response => response.json()).then(data => {
        let gameComponent = document.createElement('div');
        gameComponent.classList.add('game', 'rounded-2', 'flex-row', 'd-flex');
        let gameName = document.createElement('span');
        gameName.classList.add('score')
        gameName.textContent = `Score : ${data.score}`;
        gameComponent.appendChild(gameName);
        if (data.endTime == null) 
        {
            let gameButton = document.createElement('button');
            gameButton.classList.add('button', 'rounded-2');
            gameButton.textContent = 'Join';
            gameButton.onclick = function() {
                let url = window.location.href;
                let urlSplit = url.split('/')
                loadPage('/tournament/' + urlSplit[4] + '/game/' + game + '/');
            };
            gameComponent.appendChild(gameButton);
        }
        gameList.appendChild(gameComponent);
    });
    });
}

addMain(tournament_main);
addMain(chat_main);