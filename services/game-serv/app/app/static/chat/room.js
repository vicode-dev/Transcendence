function getRoomName() {
    let url =  window.location.pathname.split("/");
    return url[2];
}
function startChat() {
    chatArea = document.getElementById('chatArea');
    let chatSocket = new WebSocket(`wss://${window.location.host}/ws/chat/${getRoomName()}/`);
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const p = document.createElement('p');
        p.textContent = data.content;
        chatArea.appendChild(p);
    };
    chatSocket.onopen = function() {
        chatSocket.send(JSON.stringify({"type": "history"}));
    };
    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'type': 'message',
            'message': message
        }));
        messageInputDom.value = '';
    };
}
startChat() 


document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {
        document.querySelector('#chat-message-submit').click();
    }
};

