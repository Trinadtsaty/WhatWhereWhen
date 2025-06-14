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
        'question': question_ID,
    }));
};
function createQuestionMenu(arr) {
    document.getElementById("QuestionMenu").style.display = ""
    const menu = document.getElementById("QuestionMenu")
    var i=0
    console.log(arr)
    for (item in arr) {
        i++
        console.log(i)
        const button_div = document.createElement('div');
        button_div.className = 'question_button';
        button_div.textContent = i;
        button_div.onclick = () => sendQuestion(item);
        menu.appendChild(button_div);
    };
};
function closeButtonMenu() {
    document.getElementById("QuestionMenu").style.display = "none"
};
function sendQuestion(number) {
    closeButtonMenu();
    activeSocket.send(JSON.stringify({
        'question': number,
        'type' : "open_question",
    }));
};

//function windowReplace() {
////    window.location.href = window.location.href;
//    location.reload();
//
//}href="1/"


//if data['comands'] == "out":
//        await self.channel_layer.group_send(
//        self.room_group_name,
//        {
//            "type": "redirect_user",
//            "target_user_id": data['user'],
//        }
//    )
//await self.notify_all_about_users()

//async def redirect_user(self, event):
//   if event["target_user_id"] == self.user_id:
//       await self.send(text_data=json.dumps({
//           "type": "redirect",
//       }))

//group_message = {
//    'type': 'sending_question',
//    'question_name': question["question_name"],
//    'text_question': question["text_question"],
//    'note': question["note"],
//    'answer': question["answer"],
//    'answer_description': question["answer_description"],
//    'license_id': question["license_id"],
//}

//stage = {"stage":"collecting", "condition":"expectation", "message":None, "user_id": None}

//self.stage["stage"] = "get_question"
//self.stage["message"] = {
//        'question_name': event.get('question_name'),
//        'text_question': event.get('text_question'),
//        'note': event.get('note'),
//        'answer': event.get('answer'),
//        'answer_description': event.get('answer_description'),
//        'license_id': event.get('license_id'),
//    }
//self.stage["user_id"] = event["lider_id"]