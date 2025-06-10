document.addEventListener('DOMContentLoaded', function() {
    const chatSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/chat/' + room_number + '/'
    );
    // Обработчик получения сообщений
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const chatLog = document.querySelector('#chat-log');
        chatLog.innerHTML += `<div><strong>${data.username}:</strong> ${data.message}</div>`;
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    // Обработчик отправки сообщений
    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;

        chatSocket.send(JSON.stringify({
            'room_ID': room_number,
            'message': message,
            'user_id': user_id,
        }));

        messageInputDom.value = '';
    };
});