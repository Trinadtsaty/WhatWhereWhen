function cleakQuestion() {
    const setting_page = document.getElementById("settings_page")
    const player_page = document.getElementById("players_page")
    const question_page = document.getElementById("question_page")

    if (question_page.style.display === "none" && player_page.style.display === "") {
        question_page.style.display = ""
        player_page.style.display = "none"
        document.getElementById("question_button").textContent = "Игроки"
    } else if (question_page.style.display === "none" && player_page.style.display === "none" && setting_page.style.display === "") {
        question_page.style.display = ""
        setting_page.style.display = "none"
        document.getElementById("question_button").textContent = "Игроки"
        document.getElementById("settings").textContent = "Параметры"
    } else if (question_page.style.display === "") {
        question_page.style.display = "none"
        player_page.style.display = ""
        document.getElementById("question_button").textContent = "Вопросы"
    };
};

function cleaksettings() {
    const setting_page = document.getElementById("settings_page")
    const player_page = document.getElementById("players_page")
    const question_page = document.getElementById("question_page")

    if (setting_page.style.display === "none" && player_page.style.display === "") {
        setting_page.style.display = ""
        player_page.style.display = "none"
        document.getElementById("settings").textContent = "Игроки"
    } else if (setting_page.style.display === "none" && player_page.style.display === "none" && question_page.style.display === "") {
        question_page.style.display = "none"
        setting_page.style.display = ""
        document.getElementById("question_button").textContent = "Вопросы"
        document.getElementById("settings").textContent = "Игроки"
    } else if (setting_page.style.display === "") {
        setting_page.style.display = "none"
        player_page.style.display = ""
        document.getElementById("settings").textContent = "Параметры"
    };
};
function sendStart() {
//    document.querySelector('#start').onclick = function(e) {
    activeSocket.send(JSON.stringify({
        'start': "start",
    }));
//    };
};
function sendPause() {
//    document.querySelector('#pause').onclick = function(e) {
    activeSocket.send(JSON.stringify({
        'pause': "pause",
    }));
//    };
};
function sendPlay() {
//    document.querySelector('#play').onclick = function(e) {
    activeSocket.send(JSON.stringify({
        'play': "play",
    }));
//    };
};
function sendCancellation() {
//    document.querySelector('#cancellation').onclick = function(e) {
    activeSocket.send(JSON.stringify({
        'cancellation': "cancellation",
    }));
//    };
};
