let TournamentSocket
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
        console.log("LETTTSS GOOOOOO");
    } else if (actualTournament) {
        actualTournament = null;
        closeSocket();
    }
};

function openSocket(tournamentId) {
    TournamentSocket = new WebSocket(`wss://${window.location.host}/ws/tournament/${tournamentId}/`);
    console.log("Open tournament connection");
    TournamentSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        switch(data.type) {
            case "redirect":
                redirectTournament(data);
                break;
            case "stats":
                stats(data);
                break;
        }
    };
}

function closeSocket() {
    console.log("Close tournament connection");
    TournamentSocket.close();
}

function redirectTournament(data) {
    console.log("hello ")
    newUrl = data.url + window.location.search; 
    console.log(newUrl + "TEST")
    loadPage(newUrl)
}

function stats(data) {
    if (getSplitUrl().length == 4) {
        refresh(data);

    }
}

