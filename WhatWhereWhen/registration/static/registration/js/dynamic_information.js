const URL_server = 'http://127.0.0.1:8000'

function updateUser() {
    const total_users = document.querySelector("#total_users");
    const online_users = document.querySelector("#online_users");
    const questions_count = document.querySelector("#questions_count");
    const room_online = document.querySelector("#room_online");

    fetch(URL_server + '/UsersMain/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Данные не получены');
            }
            return response.json();
        })
        .then(data => {
            total_users.textContent = "Всего игроков: " + data.total_users;
            online_users.textContent = "Игроков онлайн: " + data.online_users;
            questions_count.textContent = "Всего вопросов: " + data.questions_count;
            room_online.textContent = "Активных комнат: " + data.room_online;
        })
        .catch(error => {
            console.error('Возникла проблема с операцией выборки:', error);
        });
};

const total_users_test = document.querySelector("#total_users");
if (total_users_test) {
    updateUser();
    setInterval(updateUser, 5000);
};

