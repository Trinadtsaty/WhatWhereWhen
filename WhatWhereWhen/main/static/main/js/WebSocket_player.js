
// Подключаемся к WebSocket
document.addEventListener('DOMContentLoaded', function() {
    const chatSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/chat/' + room_number + '/'
    );
    const activeSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/active/' + room_number + '/'
    );
    const peopleSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/people/' + room_number + '/'
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

    activeSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'users_list') {
            // Обработка списка пользователей
            console.log('Users in room:', data.users);
        }
    };
    if (document.querySelector('#start')) {
        document.querySelector('#start').onclick = function(e) {
            activeSocket.send(JSON.stringify({
                'start': "start",
            }));
        };
    };
    if (document.querySelector('#pause')) {
        document.querySelector('#pause').onclick = function(e) {
            activeSocket.send(JSON.stringify({
                'pause': "pause",
            }));
        };
    };

    if (document.querySelector('#play')) {
        document.querySelector('#play').onclick = function(e) {
            activeSocket.send(JSON.stringify({
                'play': "play",
            }));
        };
    };
    if (document.querySelector('#cancellation')) {
        document.querySelector('#cancellation').onclick = function(e) {
            activeSocket.send(JSON.stringify({
                'cancellation': "cancellation",
            }));
        };
    };


    activeSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log(data);
        };



    peopleSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
//        console.log(data);
//        document.getElementById("players_page")
//        console.log(data.users)
        const usersArray = data.users;
        // Очистка
        while (document.getElementById("players_page").firstChild) {
            document.getElementById("players_page").removeChild(document.getElementById("players_page").firstChild);
        }

        for (let i = 0; i < usersArray.length; i++) {
            const user = usersArray[i];
            console.log(user);
            const img = document.createElement('img');
            img.className = 'img';
            img.alt = 'Фото профиля';
            img.src = user.picture;

            const image_box = document.createElement('div');
            image_box.className = 'image_box';
//            console.log(host_id, user.id)
            if (user.id === host_id) {
                const player_host = document.createElement('div');
                player_host.textContent = 'H'
                player_host.className = 'player_host'
                image_box.appendChild(player_host);
            };
            image_box.appendChild(img);

            const player_name = document.createElement('div');
            player_name.className = 'player_name';
            player_name.textContent = user.login

            const player_role = document.createElement('div');
            player_role.className = 'player_role';
            if (user.id === captain_id) {
                player_role.textContent = 'Капитан'
            } else if (user.id === leader_id) {
                player_role.textContent = 'Ведущий'
            } else {
                player_role.textContent = 'Игрок'
            };
            const text_box = document.createElement('div');
            text_box.className = 'text_box';
            text_box.appendChild(player_name);
            text_box.appendChild(player_role);

            const button_players = document.createElement('div');
            button_players.className = 'button players';

            const player = document.createElement('div');
            player.className = 'player';

            player.appendChild(image_box);
            player.appendChild(text_box);
            player.appendChild(button_players);

            document.getElementById("players_page").appendChild(player);
        };
    };

});
