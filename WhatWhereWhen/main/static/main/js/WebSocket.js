const chatSocket = new WebSocket('ws://localhost:8000/ws/somepath/');

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data['message']);
};

chatSocket.onclose = function(e) {
    console.error('WebSocket закрыт неожиданно');
};

function sendMessage(message) {
    chatSocket.send(JSON.stringify({
        'message': message
    }));
}