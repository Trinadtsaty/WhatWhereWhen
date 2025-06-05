//const chatSocket = new WebSocket('ws://localhost:8000/ws/somepath/');
//
//chatSocket.onmessage = function(e) {
//    var data = JSON.parse(e.data);
////    document.getElementById("dinamic").textContent = data['message']
//    document.getElementById("dinamic").innerText = data.message
//    console.log(data['message']);
//};
//
//
//chatSocket.onclose = function(e) {
//    console.error('WebSocket закрыт неожиданно');
//};
//
//function sendMessage(message) {
//    chatSocket.send(JSON.stringify({
//        'message': message
//    }));
//}
const roomId = 1
const socket = new WebSocket(
    `ws://${window.location.host}/ws/game_room/${roomId}/`
);

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.type === 'user_list') {
        console.log('Пользователи в комнате:', data.users);
        console.log('Количество:', data.count);
        // Обновите UI списка пользователей
    }

    if (data.type === 'start_game') {
        console.log(data.message);
        alert('Игра начинается!');
        // Запустите игровую логику
    }
};

socket.onclose = function(e) {
    console.error('WebSocket закрыт.');
};

// При закрытии страницы
window.addEventListener('beforeunload', function() {
    socket.close();
});