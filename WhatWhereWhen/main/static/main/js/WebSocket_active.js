//document.addEventListener('DOMContentLoaded', function() {
const activeSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/active/' + room_number + '/'
);
activeSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type === 'users_list') {
        // Обработка списка пользователей
        console.log('Users in room:', data.users);
    }
};
activeSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);
    console.log(data.type)
    console.log(data.message)
};



//    function sendStart() {
//        document.querySelector('#start').onclick = function(e) {
//            activeSocket.send(JSON.stringify({
//                'start': "start",
//            }));
//        };
//    };
//    function sendPause() {
//        document.querySelector('#pause').onclick = function(e) {
//            activeSocket.send(JSON.stringify({
//                'pause': "pause",
//            }));
//        };
//    };
//    function sendPlay() {
//        document.querySelector('#play').onclick = function(e) {
//            activeSocket.send(JSON.stringify({
//                'play': "play",
//            }));
//        };
//    };
//    function sendCancellation() {
//        document.querySelector('#cancellation').onclick = function(e) {
//            activeSocket.send(JSON.stringify({
//                'cancellation': "cancellation",
//            }));
//        };
//    };

//    if (document.querySelector('#start')) {
//        document.querySelector('#start').onclick = function(e) {
//            activeSocket.send(JSON.stringify({
//                'start': "start",
//            }));
//        };
//    };
//    if (document.querySelector('#pause')) {
//        document.querySelector('#pause').onclick = function(e) {
//            activeSocket.send(JSON.stringify({
//                'pause': "pause",
//            }));
//        };
//    };
//
//    if (document.querySelector('#play')) {
//        document.querySelector('#play').onclick = function(e) {
//            activeSocket.send(JSON.stringify({
//                'play': "play",
//            }));
//        };
//    };
//    if (document.querySelector('#cancellation')) {
//        document.querySelector('#cancellation').onclick = function(e) {
//            activeSocket.send(JSON.stringify({
//                'cancellation': "cancellation",
//            }));
//        };
//    };



//});