// function username() {
//     username = document.getElementById("username").value;
//     fetch(`/api/player/${document.querySelector('[name=playerId]').value}/username/`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken,
//         },
//         body: JSON.stringify({ "username": username })
//     }).then(response => {
//         if (!response.ok) {
//             response.text().then(data => {
//                 document.getElementById("username-error").innerHTML = data;
//             });
//         }
//         else {
//             document.getElementById("username-error").innerHTML = "";
//             username = document.getElementById("username")
//             username.placeholder = username.value;
//             username.value = "";
            
//         }
//     });
// }

function sendUsername() {
    username = document.getElementById("username");
    editButton = document.getElementById("edit-username");
    saveButton = document.getElementById("save-username");

    fetch(`/api/player/${document.querySelector('[name=playerId]').value}/username/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ "username": username.value })
    }).then(response => {
        if (!response.ok) {
            response.text().then(data => {
                document.getElementById("username-error").innerHTML = data;
            });
        }
        else {
            username = document.getElementById("username")
            username.placeholder = username.value;
            username.value = "";
            editButton.style.display = "block";
            saveButton.style.display = "none";
            username.disabled = true;
            
        }
    });
}

function editUsername() {
    username = document.getElementById("username");
    editButton = document.getElementById("edit-username");
    saveButton = document.getElementById("save-username");
    editButton.style.display = "none";
    saveButton.style.display = "block";
    username.disabled = false;

}