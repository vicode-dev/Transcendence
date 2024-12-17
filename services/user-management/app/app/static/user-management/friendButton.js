async function postData(url) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body: null
    });
    
    if (!response.ok)
        throw new Error('Network response was not ok');
}

function updateBtn(action, btnText, friendId, newClass)
{
    document.getElementById("updateBtn").innerHTML = "";
    document.getElementById("friendButton").style.display = "none";
    newBtn = document.createElement("button");
    newBtn.innerHTML = btnText;
    newBtn.setAttribute("class", "rounded-2 friendButton" + newClass);
    newBtn.setAttribute("onclick", action + "(" + friendId + ")");
    newBtn.setAttribute("style", "color: var(--background-color);");
    document.getElementById("updateBtn").append(newBtn);
}

function addFriend(friendId) {
    postData("/api/friends/add?playerId=" + friendId)
    .catch(error => {
        console.error('Error:', error);
    });
    updateBtn("removeFriend", "remove as friend", friendId, " removeFriendBtn");
}

function removeFriend(friendId) {
    postData("/api/friends/remove?playerId=" + friendId)
    .catch(error => {
        console.error('Error:', error);
    });
    updateBtn("addFriend", "add as friend", friendId, " addFriendBtn");
}