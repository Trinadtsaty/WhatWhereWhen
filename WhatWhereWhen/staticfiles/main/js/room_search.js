function filterItemsSesion() {
    const input = document.getElementById('input_search');
    const filter = input.value.toLowerCase();
    const ul = document.getElementById('list_rooms');
    const li = ul.getElementsByTagName('li');

    for (let i = 0; i < li.length; i++) {
        const item = li[i].textContent || li[i].innerText;
        if (item.toLowerCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        };
    };
};
function formatQuestionText20(text) {
    // Заменяем переносы на пробелы
    text = text.replace(/\n/g, ' ');
    // Если длина текста больше 20 символов, обрезаем и добавляем "..."
    return text.length > 20 ? text.slice(0, 20) + '...' : text;
};
function formatQuestionText19(text) {
    // Заменяем переносы на пробелы
    text = text.replace(/\n/g, ' ');
    // Если длина текста больше 20 символов, обрезаем и добавляем "..."
    return text.length > 16 ? text.slice(0, 16) + '...' : text;
};
function check_description(text) {
    if (text.length === 0) {
        return "Описание комнаты"
    } else {
        return text
    }
};
function returnMode(text) {
    if (text === "0") {
        return "Классика"
    } else if (text === "1") {
        return "Спорт"
    } else {
        return "Совместный ответ"
    };
};
rooms = document.querySelectorAll(".room");
info_panel = document.getElementById("info_room");
rooms.forEach(item => {
    item.addEventListener('click', () => {
        info_panel.style.display='';
        document.getElementById("session_name_box").textContent = "Название: " + formatQuestionText20(item.dataset.name);
        document.getElementById("count_players").textContent = "Количество игроков: "+ item.dataset.users + " / " + item.dataset.limit;
        document.getElementById("room_hours").textContent = "Время на вопрос: " + item.dataset.time;
        document.getElementById("room_mode").textContent = "Режим: " + returnMode(item.dataset.mode);
        document.getElementById("room_pack_name").textContent = "Название пака: " + formatQuestionText19(item.dataset.selection);
        document.getElementById("room_description").textContent = check_description(item.dataset.description);
        if (item.dataset.password === "False") {
//            console.log("False")
            document.getElementById("link_room").href=`/game/${item.dataset.room}/`
        } else {
//            console.log("True")
            document.getElementById("link_room").href=`/game/password/?pas=${item.dataset.room}`
        };

    });
});

const leader_checkbox = document.getElementById('leader')
leader_checkbox.addEventListener('change', () => {
    const checkbox_tag = leader_checkbox.checked;
    const ul = document.getElementById('list_rooms');
    const li = ul.getElementsByTagName('li');

    if (checkbox_tag) {
        for (let i = 0; i < li.length; i++) {
            const item = li[i].dataset.leader;
            if (item === "True") {
                li[i].style.display = "none";
            } else {
                li[i].style.display = "";
            };
        };
    } else {
        for (let i = 0; i < li.length; i++) {
            li[i].style.display = "";
        };
    };
});

const password_checkbox = document.getElementById('password')
password_checkbox.addEventListener('change', () => {
    const checkbox_tag = password_checkbox.checked;
    const ul = document.getElementById('list_rooms');
    const li = ul.getElementsByTagName('li');

    if (checkbox_tag) {
        for (let i = 0; i < li.length; i++) {
            const item = li[i].dataset.password;
            if (item === "True") {
                li[i].style.display = "none";
            } else {
                li[i].style.display = "";
            };
        };
    } else {
        for (let i = 0; i < li.length; i++) {
            li[i].style.display = "";
        };
    };
});



document.getElementById("refresh_button").addEventListener("click", function() {
    location.reload(true); // Перезагрузить страницу с обновлением кэша
});
