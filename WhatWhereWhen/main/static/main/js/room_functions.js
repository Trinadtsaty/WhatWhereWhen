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
    document.getElementById("question_screen").dataset.value = data.question_id;

    if (data.time_read > 0) {
        hide_access_user()
        time_output(data.time_read)
    } else {
        show_access_user()
        time_output(data.time_question)
    };

//    time_output (data.time_read)
//    start_question_read_time(data.time_read, data.time_question)
};
function hide_access_leader() {
    document.querySelectorAll(".access_leader").forEach(item => {
        item.style.display = "none";
//        console.log("вы тут")
    });
};
function hide_access_user() {
    document.querySelectorAll(".access_user").forEach(item => {
        item.style.display = "none";
//        console.log("вы тут")
    });
};
function show_access_user() {
    if (document.getElementById("gives_answer_button")) {
        document.getElementById("gives_answer_button").pointerEvents = "";
    };
    document.querySelectorAll(".access_user").forEach(item => {
        item.style.display = "";
//        console.log("вы тут")
    });
};

function showQuestion_leader(data) {
    document.getElementById("popup_answer").style.display = "";
//    console.log("showQuestion_leader",data)
    document.getElementById("question_screen").dataset.value = data.question_id;

    if (!data.note) {
        document.getElementById("description_button").style.display = "none";
    } else {
        document.getElementById("description_button").style.display = "";
        document.getElementById("note").textContent = "Примичание: " + data.note;
    };

    if (data.time_read > 0) {
//        console.log("мы в больше нуля")
        time_output(data.time_read)
    } else {
//        console.log("мы в меньше нуля")
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

function open_answer(text) {
    document.querySelector(text).classList.toggle('show');
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
//        startTimer(time_left);pause_question_time()
//    };
//};

function pause_question_time() {
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
let canClick = true;
function pluse_question_time (value) {
    if (!canClick) return;
    canClick = false;
    activeSocket.send(JSON.stringify({
        'status_game': "pluse",
        'value' : value,
    }));
    const time = document.getElementById('timer_panel').textContent;
    const parts = time.split(":"); // ["01", "12"]
    const firstNumber = parseInt(parts[0], 10);  // 1
    const secondNumber = parseInt(parts[1], 10); // 12
    let timer = (firstNumber*60+secondNumber)+value;
    if (timer > 0) {
        time_output((firstNumber*60+secondNumber)+value);
    } else {
        time_output(1);
    }

    setTimeout(() => {
        canClick = true; // Разрешаем следующий клик через 500 мс
    }, 500);
};
function clear_chat() {
    const questions_box = document.getElementById('chat');
    while (questions_box.firstChild) {
        questions_box.removeChild(questions_box.firstChild);
    }
};

function time_output (value) {
//    console.log(value)
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

//function closeButtonAnswerBox() {
//    document.getElementById("write_answer_box_popup").style.display = "none"
//};
function closePopup(event) {
    document.getElementById('page_question').style.pointerEvents = ""
    document.getElementById('page').style.pointerEvents = ""
    event.style.display = "none"
};

function open_early_response_popup () {
    document.getElementById('page_question').style.pointerEvents = "none"
    document.getElementById('page').style.pointerEvents = "none"
    document.getElementById('write_early_response_box_popup').style.display = "";
    checkScale(document.getElementById('write_early_response_box_popup'))
};
function open_answer_popup () {
    document.getElementById('page_question').style.pointerEvents = "none"
    document.getElementById('page').style.pointerEvents = "none"
    document.getElementById('write_answer_box_popup').style.display = "";
    checkScale(document.getElementById('write_answer_box_popup'))
};
function checkScale(event) {
    const width = window.innerWidth;
    const height = window.innerHeight;

    const width_windiw = event.offsetWidth;
    const height_windiw = event.offsetHeight;

    event.style.left = `${Math.floor(width/2)-Math.floor(width_windiw/2)}px`;
    event.style.top = `${Math.floor(height/2)-Math.floor(height_windiw/2)}px`;
};

function send_answer() {
    const answer = document.getElementById('answer_input_line').value;
    const description = document.getElementById('description_answer_input_box').value;

    const checking_answer = check_answer(answer);
    if (checking_answer) {
        const checking_description = check_description(description);
        if (checking_description) {
            document.getElementById('answer_input_line').value = "";
            document.getElementById('description_answer_input_box').value = "";

            activeSocket.send(JSON.stringify({
                'question': document.getElementById("question_screen").dataset.value,
                'type' : "answer",
                'answer': answer,
                'description': description,
                'author_answer': user_id,
            }));
            closePopup(document.getElementById('write_answer_box_popup'))
        };
    };
};
function send_early_response() {
    const answer = document.getElementById('early_response_input_line').value;
    const description = document.getElementById('description_early_response_input_box').value;

    const checking_answer = check_answer(answer);
    if (checking_answer) {
        const checking_description = check_description(description);
        if (checking_description) {
            document.getElementById('early_response_input_line').value = "";
            document.getElementById('description_early_response_input_box').value = "";

            activeSocket.send(JSON.stringify({
                'question': document.getElementById("question_screen").dataset.value,
                'type' : "early_response",
                'answer': answer,
                'description': description,
                'author_answer': user_id,
            }));
            closePopup(document.getElementById('write_early_response_box_popup'))
        };
    };
};
function check_answer(text) {
    if (text.length > 100) {
        document.getElementById('claim_error').textContent = "Ответ слишком длинный, уместите его в 100 символов";
        show("claim_error");
        return false;
    } else {
        return true;
    };
};
function check_description(text) {
    if (text.length > 500) {
        document.getElementById('claim_error').textContent = "Примичание слишком длинное, уместите его в 500 символов";
        show("claim_error");
        return false
    } else {
        return true
    };
};
function create_answer(data) {
//    author_answer
    document.getElementById('popup_accepting_answer').dataset.value = data.author_answer

    document.getElementById('popup_accepting_answer').style.display = "";
    document.getElementById('popup_accepting_answer').dataset.value = data.author_answer_id;
    document.getElementById('accepting_answer').textContent = "Ответ: " + data.answer;
    document.getElementById('accepting_answer').className = data.Class_answer;
    document.getElementById('accepting_answer').style.minWidth = "625px";

    document.getElementById('accepting_answer_description').textContent = "Примичание: " + data.description;
    document.getElementById('accepting_answer_description').className = data.Class_answer;
    document.getElementById('accepting_answer_description').style.minWidth = "625px";
    document.getElementById('accepting_answer_description').style.minHeight = "260px";

    document.getElementById('buttons_like_box').onclick = send_like;
    document.getElementById('buttons_dislike_box').onclick = send_dislike;
};

function send_like() {
//    if (room_game_mode === "Спорт") {
//
//    } else {
//        const znach = document.getElementById('players_score').textContent.split(":");
//        document.getElementById('players_score').textContent = znach[0] + ": " + formatNumber(parseInt(znach[1], 10)+1);
//    };
    const znach = document.getElementById('players_score').textContent.split(":");
    document.getElementById('players_score').textContent = znach[0] + ": " + formatNumber(parseInt(znach[1], 10)+1);

    hide_after_answer()
    open_answer('#popup_accepting_answer')
    activeSocket.send(JSON.stringify({
        'status_game': "like",
        'author_answer': document.getElementById('popup_accepting_answer').dataset.value,
        "question": document.getElementById("question_screen").dataset.value,
    }));
};
function send_dislike() {
    if (room_game_mode === "Спорт") {

    } else {
        const znach = document.getElementById('authors_score').textContent.split(":");
        document.getElementById('authors_score').textContent = znach[0] + ": " + formatNumber(parseInt(znach[1], 10)+1);
    };
    hide_after_answer()
    open_answer('#popup_accepting_answer')
    activeSocket.send(JSON.stringify({
        'status_game': "dislike",
        'author_answer': document.getElementById('popup_accepting_answer').dataset.value,
        "question": document.getElementById("question_screen").dataset.value,
    }));
};
function showe_score(score) {
    const score_on_page = document.getElementById('score');
    while (score_on_page.firstChild) {
        score_on_page.removeChild(score_on_page.firstChild);
    };
    if (room_game_mode === "Спорт") {
        for (const login in score.players) {
//            console.log(score.players[login])
            const authors = document.createElement('div');
            authors.className = "score_element";
            authors.id = "authors_score";
            authors.textContent = `${login}: ${formatNumber(score.players[login])}`;
            score_on_page.appendChild(authors);
        };


    } else {
        const authors = document.createElement('div');
        authors.className = "score_element";
        authors.id = "authors_score";
        authors.textContent = `Авторы: ${formatNumber(score.authors)}`;
        score_on_page.appendChild(authors);
        const player = document.createElement('div');
        player.className = "score_element";
        player.id = "players_score";
        player.textContent = `Игроки: ${formatNumber(score.players)}`;
        score_on_page.appendChild(player);
    };
//    document.getElementById('score').textContent = `${formatNumber(score.authors)}:${formatNumber(score.players)}`;
};
function hide_after_answer() {
    document.getElementById("popup_answer").style.display = "none";
    document.getElementById("popup_accepting_answer").style.display = "none";
};
function send_captain_chose(number) {
//    console.log("ты кликнул сюда")
    document.getElementById("gives_answer_button").pointerEvents = "none";
    document.getElementById("satisfy").style.display = "none";
    activeSocket.send(JSON.stringify({
        'question': number,
        'type': "captain_chose_your",
    }));
};
function open_answeing() {
//    satisfy
    document.getElementById("satisfy").style.display = "";
    pause_question_time();
};
function create_answer_arr(data) {
    document.getElementById('popup_accepting_answer').style.display = "";
    ///static/main/img/like.png
    ///static/main/img/dislike.png
    //button_div.onclick = () => sendQuestion(item);
    const answer_box = document.getElementById("part_answers_box");
    while (answer_box.firstChild) {
        answer_box.removeChild(answer_box.firstChild);
    };
    const button_users_answering = document.createElement('div');
    button_users_answering.id = "button_users_answering"
    button_users_answering.className = "scroll";
    answer_box.appendChild(button_users_answering);

    const accepting_answer = document.createElement('div');
    accepting_answer.id = "accepting_answer";

    const accepting_answer_description = document.createElement('div');
    accepting_answer_description.id = "accepting_answer_description";
    accepting_answer_description.className = "scroll";

    const text_box = document.createElement('div');
    text_box.appendChild(accepting_answer);
    text_box.appendChild(accepting_answer_description);
    answer_box.appendChild(text_box);

    // console.log("выводим массив ответов",data)
    let chek_answer = true
    for (let i = 0; i < data.length; i++) {
        console.log(data[i]);
        if (!isIdInArray(data[i].author_answer_id, accepted_responses_arr)) {
            const element_users_answering = document.createElement('div');
            element_users_answering.className = "element_users_answering";
            element_users_answering.id = `user_answer_id_${data[i].author_answer_id}`
            element_users_answering.textContent = data[i].author_answer;
            element_users_answering.onclick = () => CreateAnswer(data[i]);

            button_users_answering.appendChild(element_users_answering);
            if (chek_answer) {
                element_users_answering.click();
                chek_answer = false
            };
        };
    };
    if (chek_answer) {
        document.getElementById('popup_accepting_answer').style.display = "none";
    };
};
function CreateAnswer(data) {
    document.getElementById('accepting_answer').textContent = "Ответ: " + data.answer;
    document.getElementById('accepting_answer').className = data.Class_answer;

    document.getElementById('accepting_answer_description').textContent = "Примичание: " + data.description;
    document.getElementById('accepting_answer_description').className = data.Class_description;

    document.getElementById('buttons_like_box').onclick = () => send_like_sport(data.author_answer_id);
    document.getElementById('buttons_dislike_box').onclick = () => send_dislike_sport(data.author_answer_id);
};
function send_like_sport(author_id) {
    accepted_responses_arr.push(author_id);
//    if (accepted_responses_arr.length === answer_arr.length) {
//        document.getElementById('popup_accepting_answer').style.display = "none";
//    };
    document.getElementById(`user_answer_id_${author_id}`).style.display = "none";
    let chek = true
    const buttons = document.querySelectorAll(".element_users_answering").forEach(item => {
        if (item.style.display != "none" && chek) {
            item.click();
            chek = false;
        };
    });
    if (chek) {
        document.getElementById('popup_accepting_answer').style.display = "none";
    };

    activeSocket.send(JSON.stringify({
        'status_game': "like",
        'author_answer': author_id,
        "question": document.getElementById("question_screen").dataset.value,
    }));
}
function send_dislike_sport(author_id) {
    accepted_responses_arr.push(author_id);
//    if (accepted_responses_arr.length === answer_arr.length) {
//        document.getElementById('popup_accepting_answer').style.display = "none";
//    };
    document.getElementById(`user_answer_id_${author_id}`).style.display = "none";
    let chek = true
    const buttons = document.querySelectorAll(".element_users_answering").forEach(item => {
        if (item.style.display != "none" && chek) {
            item.click();
            chek = false;
        };
    });
    if (chek) {
        document.getElementById('popup_accepting_answer').style.display = "none";
    };


    activeSocket.send(JSON.stringify({
        'status_game': "dislike",
        'author_answer': author_id,
        "question": document.getElementById("question_screen").dataset.value,
    }));
}

function isIdInArray(id, arr) {
    if (!Array.isArray(arr)) {
        return false;
    };
    return arr.includes(id);
};
function containsKey(key, tuple) {
  if (!tuple || typeof tuple !== 'object') {
    return false;
  }
  return Object.prototype.hasOwnProperty.call(tuple, key);
}
function NextQuestion() {
    activeSocket.send(JSON.stringify({
        'question': "random_question",
        'type' : "random_question",
    }));
};
function show_timer(value) {
    const timerElement = document.getElementById('timer');
    timerElement.textContent = value;
    timerElement.style.display = "";
};



function jointResponse_like(author_id) {
    activeSocket.send(JSON.stringify({
        'status_game': "like",
        'type': "captan",
        'author_answer': author_id,
        "question": document.getElementById("question_screen").dataset.value,
    }));
};
function jointResponse_dislike(author_id) {
    activeSocket.send(JSON.stringify({
        'status_game': "dislike",
        'type': "captan",
        'author_answer': author_id,
        "question": document.getElementById("question_screen").dataset.value,
    }));
};