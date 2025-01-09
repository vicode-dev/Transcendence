let chatSocket

function chat_main() {
    document.querySelector('#chat-message-input').focus();
    destructors.push(chat_destructor);
    let chatArea = document.getElementById('messageArea');
    let chat = document.getElementById('chat');
    const navbar = document.getElementById('nav');
    const navBarHeight = navbar.offsetHeight + parseInt(getComputedStyle(navbar).marginBottom) + parseInt(getComputedStyle(navbar).marginTop);
    chat.style.setProperty('--bottom-margin', navBarHeight + 'px');
    chatSocket = new WebSocket(`wss://${window.location.host}/ws/chat/${document.querySelector('[name=chatId]').value}/`);
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        fetch("/api/player/" + data.playerId + "/username/")
        .then(response => response.json())
        .then(username => {
            const messageComponent = document.createElement('div');
            messageComponent.classList.add('messageComponent', 'd-flex', 'align-items-start', 'mb-2');
            
            const avatar = document.createElement('img');
            avatar.classList.add('usr-img', 'mr-2');
            avatar.src = `/api/player/${data.playerId}/avatar`;
            avatar.style.height = '2rem';
            avatar.style.width = '2rem';
            avatar.style.borderRadius = '50%';
            
            const messageContent = document.createElement('div');
            messageContent.classList.add('message-content');
            
            const messageHeader = document.createElement('div');
            messageHeader.classList.add('d-flex', 'justify-content-between');
            
            const usernameElement = document.createElement('p');
            usernameElement.classList.add('username', 'mb-0');
            usernameElement.textContent = username.username;
            
            const messageDate = document.createElement('span');
            messageDate.classList.add('message-date');
            messageDate.textContent = new Date(data.timestamp).toLocaleString([], {hourCycle: 'h23', hour: '2-digit', minute: '2-digit' });
            
            const messageText = document.createElement('p');
            messageText.classList.add('message-text', 'mb-0');
            messageText.textContent = data.content;
            
            messageHeader.appendChild(usernameElement);
            messageHeader.appendChild(messageDate);
            messageContent.appendChild(messageHeader);
            messageContent.appendChild(messageText);
            messageComponent.appendChild(avatar);
            messageComponent.appendChild(messageContent);
            chatArea.appendChild(messageComponent);
            chatArea.scrollTop = chatArea.scrollHeight;
        });
    };
    chatSocket.onopen = function() {
        chatSocket.send(JSON.stringify({"type": "history"}));
    };
    chatSocket.onclose = function(e) {
        if (e.wasClean == false)
        console.error('Chat socket crashed', e);
    };
}

function sendMessage() {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (message.length === 0) {
        return;
    }
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message': message
    }));
    messageInputDom.value = '';
};

function sendMessageOnEnter(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
}

function chat_destructor() {
    console.log("Destructor");
    chatSocket.close();
    chatSocket = null;
}

addMain(chat_main);
