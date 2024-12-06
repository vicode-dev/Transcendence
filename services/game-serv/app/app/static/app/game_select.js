// window.addEventListener('DOMContentLoaded', function () {
    document.getElementById('pong-content').style.display ='none';
    document.getElementById('online-content').style.display = 'none';

// })

function hidePong () {
    document.getElementById('pong-content').style.display ='none';
    pongRequiredInputs = document.getElementsByClassName('pong-required');
    for (const pongRequiredInput of pongRequiredInputs) {
        pongRequiredInput.removeAttribute("required");
    }
}

function showPong () {
    document.getElementById('pong-content').style.display ='block';
    pongRequiredInputs = document.getElementsByClassName('pong-required');
    for (pongRequiredInput of pongRequiredInputs) {
        pongRequiredInput.setAttribute("required", "");
    }
}

function showRender () {
    document.getElementById('online-content').style.display = 'block';
    pongRequiredInputs = document.getElementsByClassName('online-required');
    for (pongRequiredInput of pongRequiredInputs) {
        pongRequiredInput.setAttribute("required", "");
    }
}

function hideRender () {
    document.getElementById('online-content').style.display = 'none';
    pongRequiredInputs = document.getElementsByClassName('online-required');
    for (pongRequiredInput of pongRequiredInputs) {
        pongRequiredInput.removeAttribute("required", "");
    }
}

const   formButton = document.getElementById('submit-form');
formButton.style.display = "none";
document.getElementById('game-form').addEventListener('input', function() {
    const   isFormValid = document.getElementById('game-form').checkValidity();
    if (isFormValid)
    {
        formButton.style.display = "block";
        // formButton.style.backgroundColor = accentColor;
        // formButton.style.color = secondaryColor;
    }
    // else
    // {
    //     formButton.style.backgroundColor = secondaryColor;
    //     formButton.style.color = "white";
    // }
})


//TO DO fix that later
const inputOne = document.getElementById('connect4');
const inputTwo = document.getElementById('pong');

inputOne.addEventListener('click', hoverTest);
inputTwo.addEventListener('click', hoverTest);

function hoverTest() {
    console.log('click');
    // if (inputTwo.checked) {
    inputTwo.addEventListener('mouseover', test2);
    // }
}

function test2() {
    console.log('test');
    document.querySelector('.one + .input-label .input-content').style.backgroundColor = 'tomato';
}


// const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// async function postData(url = '', data = {}) {
// const response = await fetch(url, {
//     method: 'POST',
//     headers: {
//         'X-CSRFToken': csrftoken,
//         'Content-Type': 'application/json'
//     },
//     mode: 'same-origin',
//     body: JSON.stringify(data)
// });

// if (!response.ok)
//     throw new Error('Network response was not ok');
// return response.json();
// }

// function create(event) {
//     let gameType = document.querySelector('input[type=radio][name=gameType]:checked').value;
//     let maxPlayers = document.querySelector('input[type=radio][name=maxPlayers]:checked').value;
//     let render = document.querySelector('input[type=radio][name=render]:checked').value;
    
//     // postData('/game/local', { maxPlayers: maxPlayers, gameType: gameType, render: render })
//     // .then(data => {
//     //     let Game = JSON.parse(data)
//     //     // room_url = "/lobby/" + Game[0].pk;
//     //     loadPageEvent(event, '/game/local');
//     // })
//     // .catch(error => {
//     //     console.error('Error:', error);
//     // });
// }

// const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
// document.getElementById('game-form').addEventListener('submit', function(event) {
//     event.preventDefault();

//     const gameType = document.querySelector('input[type=radio][name=gameType]:checked').value;
//     const maxPlayers = document.querySelector('input[type=radio][name=maxPlayers]:checked').value;
//     const render = document.querySelector('input[type=radio][name=render]:checked').value;
//     const data = {
//         gameType: gameType,
//         maxPlayers: maxPlayers,
//         render: render
//     };

//     fetch('/game/local/', {
//         method: 'POST',
//         headers: {
//             'X-CSRFToken': csrftoken,
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data),
//     })
//     .then(response => response.json())
//     .then(responseData => {
//         console.log('Success:', responseData);
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// });


// let urls = {
//     localgame: "{% url 'localgame' %}",
// };

// function loadLocalGame(event) {
//     const gameType = document.querySelector('input[type=radio][name=gameType]:checked').value;
//     let maxPlayers= 0;
//     let render = 0;
//     if (gameType != 1)
//     {
//         maxPlayers = document.querySelector('input[type=radio][name=maxPlayers]:checked').value;
//         render = document.querySelector('input[type=radio][name=render]:checked').value;
//     }
//     if (gameType == 1)
//         loadPageEvent(event, urls.localgame);
//     //render connect4
//     // else {
//     //     if (maxPlayers == 2 && render == 1)
//     //         loadPageEvent(event, "partials/connect4.html")
//     //         //render pong 2P 2D
//     //     if (maxPlayers == 2 && render == 0)
//     //         //render pong 2P 3D
//     //     if (maxPlayers == 4 && render == 1)
//     //         //render pong 4P 2D
//     //     if (maxPlayers == 4 && render == 0)
//     //         //render pong 4P 3D
//     // }
// }


function loadLocalGame(event, localgameUrl) {
    // const localgameUrl = urls.localgame;
    const url = new URL(localgameUrl, window.location.href);

    const gameType = document.querySelector('input[type=radio][name=gameType]:checked').value;
    url.searchParams.append('gameType', gameType);

    if (gameType == 0)
    {
        const maxPlayers = document.querySelector('input[type=radio][name=maxPlayers]:checked').value;
        let render = 0;
        if (document.querySelector('input[type=radio][name=render]:checked'))
        {
            render = document.querySelector('input[type=radio][name=render]:checked').value;
            url.searchParams.append('render', render);
        }
        url.searchParams.append('maxPlayers', maxPlayers);
    }
    loadPageEvent(event, url.toString());
}