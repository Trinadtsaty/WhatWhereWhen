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
    document.getElementById("start").style.display = "none";
    document.getElementById("cancellation").style.display = "";
    activeSocket.send(JSON.stringify({
        'status_game': "start",
    }));
//    };
};
function sendPause() {
//    document.querySelector('#pause').onclick = function(e) {
    activeSocket.send(JSON.stringify({
        'status_game': "pause",
    }));
//    };
};
function sendPlay() {
//    document.querySelector('#play').onclick = function(e) {
    activeSocket.send(JSON.stringify({
        'status_game': "play",
    }));
//    };
};
function sendCancellation() {
    document.getElementById("cancellation").style.display = "none";
    document.getElementById("start").style.display = "";
//    document.querySelector('#cancellation').onclick = function(e) {
    activeSocket.send(JSON.stringify({
        'status_game': "cancellation",
    }));
//    };
};
function submitForm() {
    document.getElementById("accept_additional_settings").click();
    if (window.history.replaceState) {
//        setTimeout(windowReplace(), 3000);
//        window.history.replaceState(null, null, window.location.href);
    };
};
function deleteQuestion(question_ID) {
    activeSocket.send(JSON.stringify({
        'type': "delete",
        'question': question_ID,
    }));
};
function hide_all() {
//    document.getElementById("question_page").style.display = "none"
//    document.getElementById("page").style.display = "none"
    const questionPage = document.getElementById("question_page");
    const page = document.getElementById("page");

    if (questionPage && page) {
        questionPage.style.display = "none";
        page.style.display = "none";
        console.log("Элементы скрыты");
    } else {
        console.error("Элементы не найдены:", { questionPage, page });
    }
};

function createQuestionMenu(arr) {

    const questions_box = document.getElementById('QuestionMenu');
    while (questions_box.firstChild) {
        questions_box.removeChild(questions_box.firstChild);
    }


    document.getElementById("QuestionMenu").style.display = ""
    const menu = document.getElementById("QuestionMenu")


    var i=0
    for (const item of arr.all) {
        i++
        const button_div = document.createElement('div');
        button_div.id = `question_button_${item}`
        button_div.className = 'question_button';
        button_div.textContent = i;
        button_div.onclick = () => sendQuestion(item);
//        console.log(arr.all)
//        console.log(arr.use)
//        console.log("item",item)
//        console.log("arr.use.includes(item)",arr.use.includes(item))
        if (arr.use.includes(item)) {
            button_div.style.backgroundColor = 'rgba(82, 79, 82, 1)';
            button_div.style.color = 'black';
            button_div.style.border = '3px solid rgba(33, 32, 32, 1)';
//            button_div.style.pointerEvents = 'none';
        };
        menu.appendChild(button_div);
    };
};
function closeButtonMenu() {
    document.getElementById("QuestionMenu").style.display = "none"
};
function sendQuestion(number) {
//    console.log(number)
    const button = document.getElementById(`question_button_${number}`)
    button.style.backgroundColor = 'rgba(82, 79, 82, 1)';
    button.style.color = 'black';
    button.style.border = '3px solid rgba(33, 32, 32, 1);';
    button.style.pointerEvents = 'none';

    closeButtonMenu();
    activeSocket.send(JSON.stringify({
        'question': number,
        'type' : "open_question",
    }));
};

function showQuestion_user(data) {
    console.log("showQuestion_user",data)
    document.getElementById("question_name").textContent = `Вопрос №${data.question_number}: `+ data.question_name
    document.getElementById("question_text").textContent = data.text_question

    if (data.time_read > 0) {
        time_output(data.time_read)
    } else {
        time_output(data.time_question)
    }

//    time_output (data.time_read)
//    start_question_read_time(data.time_read, data.time_question)
};
function hide_access_leader() {
    document.querySelectorAll(".access_leader").forEach(item => {
        item.style.display = "none";
        console.log("вы тут")
    });
};
function hide_access_user() {
    document.querySelectorAll(".access_user").forEach(item => {
        item.style.display = "none";
        console.log("вы тут")
    });
};

function showQuestion_leader(data) {
    document.getElementById("popup_answer").style.display = "";
    console.log("showQuestion_leader",data)
    if (!data.note) {
        document.getElementById("description_button").style.display = "none";
    } else {
        document.getElementById("note").textContent = "Примичание: " + data.note;
    };

    if (data.time_read > 0) {
        console.log("мы в больше нуля")
        time_output(data.time_read)
    } else {
        console.log("мы в меньше нуля")
        console.log(data.time_question)
        time_output(data.time_question)
    }

    document.getElementById("page_question").style.display = "";

    document.getElementById("answer").textContent = "Ответ: " + data.answer
    document.getElementById("answer_description").textContent = "Примичание: " + data.answer_description

    document.getElementById("question_name").textContent = `Вопрос №${data.question_number}: `+ data.question_name
    document.getElementById("question_text").textContent = data.text_question

//    time_output(data.time_read)
//    start_question_read_time(data.time_read, data.time_question)

};

function hide_element() {
//    hide_access_leader()
    document.getElementById("page").style.display = "none";
    document.getElementById("page_question").style.display = "";
};
function showe_element() {
    document.getElementById("page").style.display = "";
    document.getElementById("page_question").style.display = "none";
};

function open_answer() {
    document.querySelector('#popup_answer').classList.toggle('show');
};
function click_answer() {
    document.querySelector('#answer_box').style.display = "";
    document.querySelector('#note_box').style.display = "none";

    document.querySelector('#answer_show_button').style.backgroundColor = "rgba(136, 128, 136, 1)";
    document.querySelector('#note_button').style.backgroundColor = "rgba(82, 79, 82, 1)";

    document.querySelector('#answer_show_button').style.top = "0px";
    document.querySelector('#note_button').style.top = "-3px";
};
function click_note() {
    document.querySelector('#answer_box').style.display = "none";
    document.querySelector('#note_box').style.display = "";

    document.querySelector('#answer_show_button').style.backgroundColor = "rgba(82, 79, 82, 1)";
    document.querySelector('#note_button').style.backgroundColor = "rgba(136, 128, 136, 1)";

    document.querySelector('#answer_show_button').style.top = "-3px";
    document.querySelector('#note_button').style.top = "0px";
};
function send_menu() {
    activeSocket.send(JSON.stringify({
        'question': "pass",
        'type': "get_menu",
    }));
};

//let timer;
//let time_left;
//let time_question;
//let isPaused = false;


//function start_question_read_time (time_reade, time_questions) {
//    time_left = time_reade;
//    time_question = time_questions;
//    startTimer(time_left);
//    play_question_time ()
//};
//function start_question_time () {
//    time_left = time_question;
//    time_question = null;
//    if (time_left != 0) {
//        startTimer(time_left);
//    };
//};

function pause_question_time () {

    isPaused = true;
    activeSocket.send(JSON.stringify({
        'status_game': "pause",
    }));
    console.log("press_pause");

};

function play_question_time () {
    isPaused = false;
    activeSocket.send(JSON.stringify({
        'status_game': "play",
    }));
    console.log("press_play");
};

function pluse_question_time (value) {
    activeSocket.send(JSON.stringify({
        'status_game': "pluse",
        'value' : value,
    }));
};
//function startTimer (time_question) {
//    if (isPaused) return; // Если таймер на паузе, не запускаем его
//
//    timer = setInterval(() => {
//        if (time_left <= 0) {
//            clearInterval(timer);
//            start_question_time()
//            console.log("Время вышло!");
//            if (time_left <0) {
//                time_output(0)
//            };
//        } else {
//            time_left--;
//            time_output(time_left)
//        }
//    }, 1000);
//};
function clear_chat() {
    const questions_box = document.getElementById('chat');
    while (questions_box.firstChild) {
        questions_box.removeChild(questions_box.firstChild);
    }
};

function time_output (value) {
    console.log(value)
    const min = Math.floor(value / 60);
    const sec = value - (min * 60);
    document.getElementById('timer_panel').textContent = `${formatNumber(min)}:${formatNumber(sec)}`

}
function formatNumber(num) {
    // Проверяем, является ли число однозначным
    if (num >= 0 && num < 10) {
        return '0' + num; // Добавляем ноль перед однозначным числом
    };
    return num.toString(); // Возвращаем число как строку, если оно не однозначное
};

