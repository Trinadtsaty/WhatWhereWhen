
// Подключаемся к WebSocket
document.addEventListener('DOMContentLoaded', function() {
    const peopleSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/people/' + room_number + '/'
    );

    peopleSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
//        console.log(data);
//        document.getElementById("players_page")
//        console.log(data.users)
        const usersArray = data.users;
        // Очистка
        while (document.getElementById("players_page").firstChild) {
            document.getElementById("players_page").removeChild(document.getElementById("players_page").firstChild);
        };
        let user_host = false;
        let user_leader = false;
        let user_captain = false;

        for (let i = 0; i < usersArray.length; i++) {
            const user = usersArray[i];
            if (user_id === user.id && user.host) {
                user_host = true;
            };
            if (user_id === user.id && user.captain) {
                user_captain = true;
            };
            if (user_id === user.id && user.leader) {
                user_leader = true;
            };
        };
        while (document.getElementById('button_page').firstChild) {
            document.getElementById('button_page').removeChild(document.getElementById('button_page').firstChild);
        }
//        console.log("user_leader=",user_leader)
//        console.log("user_captain=",user_captain)
//        console.log("user_host=",user_host)


        for (let i = 0; i < usersArray.length; i++) {
            const user = usersArray[i];
//            console.log(user);


            const img = document.createElement('img');
            img.className = 'img';
            img.alt = 'Фото профиля';
            img.src = user.picture;

            const image_box = document.createElement('div');
            image_box.className = 'image_box';
//            console.log(host_id, user.id)
            if (user.host) {
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
            if (user.captain) {
                player_role.textContent = 'Капитан'
            } else if (user.leader) {
                player_role.textContent = 'Ведущий'
            } else {
                player_role.textContent = 'Игрок'
            };
            const text_box = document.createElement('div');
            text_box.className = 'text_box';
            text_box.appendChild(player_name);
            text_box.appendChild(player_role);

            const player = document.createElement('div');
            player.className = 'player';

            player.appendChild(image_box);
            player.appendChild(text_box);

            if (user_host) {
                const button_players = document.createElement('div');
                button_players.className = 'button players';
//                button_players.onclick = () => sendCaptain(user.id);
                player.appendChild(button_players);

                const spis_buttons = document.createElement('ul');
                spis_buttons.className = 'tools_menu';

//                let user_host = false;
//                let user_leader = false;
//                let user_captain = false;
//                console.log("!data.leader && !data.captain", !user.leader && !user.captain)
//                console.log("data.leader || data.captain", user.leader || user.captain)
//                console.log("!data.host", !user.host)
//                console.log(user_host)


                if (!user.leader && !user.captain) {
                    const buttons_leader = document.createElement('li');
                    buttons_leader.className = 'tools_element';
                    buttons_leader.textContent = 'Назначить ведущим';
                    buttons_leader.onclick = () => sendLeader(user.id);
                    spis_buttons.appendChild(buttons_leader);

                    const buttons_captain = document.createElement('li');
                    buttons_captain.className = 'tools_element';
                    buttons_captain.textContent = 'Назначить Капитаном';
                    buttons_captain.onclick = () => sendCaptain(user.id);
                    spis_buttons.appendChild(buttons_captain);
                };

                if (user.leader || user.captain) {
                    const buttons_player = document.createElement('li');
                    buttons_player.className = 'tools_element';
                    buttons_player.textContent = 'Назначить игроком';
                    buttons_player.onclick = () => sendPlayer(user.id);
                    spis_buttons.appendChild(buttons_player);
                };

                if (!user.host) {
                    const buttons_host = document.createElement('li');
                    buttons_host.className = 'tools_element';
                    buttons_host.textContent = 'Назначить Хостом';
                    buttons_host.onclick = () => sendHost(user.id);
                    spis_buttons.appendChild(buttons_host);
                };

                player.appendChild(spis_buttons);
            };

            document.getElementById("players_page").appendChild(player);
        };
        const button_page = document.getElementById("button_page")
        if (user_leader) {
            const question_button = document.createElement('div');
            question_button.className = 'button button_page_element';
            question_button.textContent = 'Вопросы';
            question_button.id = 'question_button';
            question_button.onclick = cleakQuestion;

            button_page.appendChild(question_button);
        };
        if (user_host) {
            const settings = document.createElement('div');
            settings.className = 'button button_page_element';
            settings.id = 'settings';
            settings.textContent = 'Параметры';
            settings.onclick = cleaksettings;

            const start = document.createElement('div');
            start.className = 'button button_page_element';
            start.id = 'start';
            start.textContent = 'Старт';
            start.onclick = sendStart;

            const cancellation = document.createElement('div');
            cancellation.className = 'button button_page_element';
            cancellation.id = 'cancellation';
            cancellation.textContent = 'Отмена';
            cancellation.onclick = sendCancellation;

            button_page.appendChild(settings);
            button_page.appendChild(start);
            button_page.appendChild(cancellation);
        };
    };

    function sendHost (user_id) {
        peopleSocket.send(JSON.stringify({
            'comands' : "host",
            'user' :user_id,
        }));
    };
    function sendLeader(user_id) {
        peopleSocket.send(JSON.stringify({
            'comands' : "leader",
            'user' :user_id,
        }));
    };
    function sendCaptain (user_id) {
        peopleSocket.send(JSON.stringify({
            'comands' : "captain",
            'user' : user_id,
        }));
    };
    function sendPlayer (user_id) {
        peopleSocket.send(JSON.stringify({
            'comands' : "player",
            'user' : user_id,
        }));
    };
});
