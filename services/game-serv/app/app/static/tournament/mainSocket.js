let TournamentSocket = null;
let actualTournament = null
function getSplitUrl() {
    let url =  window.location.pathname.split("/");
    return url;
}

function checkTournament() {
    url = getSplitUrl();
    const regex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    if(url[1] == "tournament" && regex.test(url[2]))
    {
        switch(actualTournament) {
            case null:
                actualTournament = url[2];
                openSocket(url[2]);
                break;
            case url[2]:
                break;
            default:
                closeSocket();
                openSocket(url[2]);
                break;    
        }
    } else if (actualTournament) {
        actualTournament = null;
        closeSocket();
    }
};

function openSocket(tournamentId) {
    TournamentSocket = new WebSocket(`wss://${window.location.host}/ws/tournament/${tournamentId}/`);
    console.log("Open tournament connection");
    TournamentSocket.addEventListener('message', receiveMessage);
}

function receiveMessage(e) {
    const data = JSON.parse(e.data);
    switch(data.type) {
        case "redirect":
            redirectTournament(data);
            break;
        case "stats":
            stats(data);
            break;
    }
}

function closeSocket() {
    console.log("Close tournament connection");
    TournamentSocket.removeEventListener('message', receiveMessage);
    TournamentSocket.close();
    TournamentSocket = null;
}

function redirectTournament(data) {
    let newUrl = data.url + window.location.search; 
    loadPage(newUrl).then();
}

function stats(data) {
    if (getSplitUrl().length == 4) {
        tournament_refresh(data);
    } 
    else if (getSplitUrl().length == 5 && getSplitUrl()[5] == "dashboard") {
        playersTree(data);
        gameList(data);
    }
}

function reconnect() {
    if(TournamentSocket.readyState != WebSocket.OPEN)
    {
        TournamentSocket.addEventListener('open', reconnect);
    }
    else
    {
        console.log("Reconnect to tournament")
        TournamentSocket.removeEventListener('open', reconnect);
        TournamentSocket.send(JSON.stringify({"type": "reconnect"}))
    }
}

