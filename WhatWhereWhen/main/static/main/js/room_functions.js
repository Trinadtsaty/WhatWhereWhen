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
function createQuestionMenu(arr) {
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

        if (arr.use.includes(item)) {
            button_div.style.backgroundColor = 'rgba(82, 79, 82, 1)';
            button_div.style.color = 'black';
            button_div.style.border = '3px solid rgba(33, 32, 32, 1);';
            button_div.style.pointerEvents = 'none';
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
    document.querySelectorAll(".access_leader").forEach(item => {
        item.style.display = "none";
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
    document.getElementById("page_question").style.display = "";

    document.getElementById("answer").textContent = "Ответ: " + data.answer
    document.getElementById("answer_description").textContent = "Примичание: " + data.answer_description

    document.getElementById("question_name").textContent = `Вопрос №${data.question_number}: `+ data.question_name
    document.getElementById("question_text").textContent = data.text_question

};

function hide_element() {
    document.getElementById("page").style.display = "none";
    document.getElementById("page_question").style.display = "";
};
function open_answer() {
    document.querySelector('#popup_answer').classList.toggle('show');
};
function click_answer() {
    document.querySelector('#answer_box').style.display = "";
    document.querySelector('#note_box').style.display = "none";

    document.querySelector('#answer_button').style.backgroundColor = "rgba(136, 128, 136, 1)";
    document.querySelector('#note_button').style.backgroundColor = "rgba(82, 79, 82, 1)";

    document.querySelector('#answer_button').style.top = "0px";
    document.querySelector('#note_button').style.top = "-3px";
};
function click_note() {
    document.querySelector('#answer_box').style.display = "none";
    document.querySelector('#note_box').style.display = "";

    document.querySelector('#answer_button').style.backgroundColor = "rgba(82, 79, 82, 1)";
    document.querySelector('#note_button').style.backgroundColor = "rgba(136, 128, 136, 1)";

    document.querySelector('#answer_button').style.top = "-3px";
    document.querySelector('#note_button').style.top = "0px";
};

