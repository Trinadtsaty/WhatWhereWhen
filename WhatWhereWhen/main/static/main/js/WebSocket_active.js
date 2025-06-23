//document.addEventListener('DOMContentLoaded', function() {
const activeSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/active/' + room_number + '/'
);
activeSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);

    if (data.type === "time") {
        if (data.Class === "break_between_questions") {
            console.log("Мы тут",data.time)
            show_timer(data.time)
            if (data.time == 0) {
                document.getElementById('timer').style.display = "none";
            };
        } else {
            time_output(data.time)
        };
        if (data.Class === "time_question" && user_id != data.leader_id) {
            show_access_user()
            if (room_game_mode === "Классика") {
                if (data.time === 0 && user_id === data.captain_id) {
                    open_answeing()
                };
            } else if (room_game_mode === "Спорт") {
                if (data.time === 0) {
                    open_answer_popup()
                };
            } else if (room_game_mode === "Совместный ответ") {
                if (data.time === 0) {
                    open_answer_popup()
                };
            };

        } else if (data.Class === "time_read") {
//            hide_access_user()
        };
    };
    if (data.type === 'score') {
        const data_2 = {
            "authors": data.score_authors,
            "players": data.score_players,
        };
        showe_score(data_2)
        if (user_id === data.leader_id) {

        } else {
//            Если режим не "Спорт" выводим сообщение о правильном или не правильном ответе
            if (room_game_mode != "Спорт") {
                document.getElementById('show_messege_people').textContent = data.status;
                document.getElementById('show_messege_people').className = data.Class;
                show("show_messege_people")
            };
        };
    };
    if (data.type === "return") {
        open_answer_popup()
    };
    if (data.type === "start_timer") {
        startCountdown(data.message);
    };
//    # Отмена стартового таймера
    if (data.type === "cancellation") {
        cancelCountdown()
    };

    if (data.type === "question_menu") {
        hide_all()
        if (user_id === data.user_id) {

            hide_element()
            createQuestionMenu(data.message)
        };
    };
    if (data.type === "return_answer") {
        pause_question_time()
        if (room_game_mode === "Спорт") {
            // Спорт
//            console.log("Спорт")
            answer_arr.push(data);
            console.log(answer_arr)
            create_answer_arr(answer_arr)
        } else if (room_game_mode === "Совместный ответ") {
            if (user_id === data.captain_id) {

                answer_arr.push(data);
//                console.log(answer_arr)
//                create_answer_captain(answer_arr)
                if (!check_send_answer) {
                    create_answer_captain(answer_arr)
                };

            } else {
                create_answer(data)
            }
        } else {
            // Классика
//            console.log(room_game_mode)
            create_answer(data)
        };

    };
    if (data.type === "random_question") {
        activeSocket.send(JSON.stringify({
            'question': data.question_number,
            'type' : "open_question",
        }));
    };

    if (data.type === "get_question") {
        answer_arr = []
        if (room_game_mode === "Совместный ответ") {
            check_send_answer = false
        };
        if (clear_chat_check) {
            clear_chat()
        };
        hide_element()
        if (user_id === data.user_id) {
            hide_access_user()
            showQuestion_leader(data)
        } else {
//            document.getElementById('page_question').style.pointerEvents = ""
//            document.getElementById('page').style.pointerEvents = ""
            hide_access_leader()
            showQuestion_user(data)
        };
    };
    if (data.type === "status_room") {
        showe_score(data.score)
        if (data.stage === "collecting") {
            // Вышел за хлебом
            console.log("Вышел за хлебом")
            showe_element()
            //            document.getElementById('page_question').style.pointerEvents = ""
            //            document.getElementById('page').style.pointerEvents = ""
        } else if (data.stage === "question_menu") {
            if (user_id === data.user_id) {
                hide_element()
                createQuestionMenu(data.message)
            } else {
                hide_all()
            };
        } else if (data.stage === "random_question") {
            activeSocket.send(JSON.stringify({
                'question': data.message,
                'type' : "open_question",
            }));
        } else if (data.stage === "get_question") {
            document.getElementById("write_answer_box_popup").style.display = "none";
            document.getElementById("write_early_response_box_popup").style.display = "none";
            let checking_popup = false;
            if (data.message.your_response === user_id && room_game_mode === "Классика") {
//                Поле введите ответ
                open_answer_popup();
                checking_popup = true;
            };
            if (room_game_mode === "Классика") {
                if (data.message.time_question === 0 && data.captain_id === user_id && !checking_popup) {
                    // Плашка капитана с выбором отвечающих
                    open_answeing()
                };
            } else if (room_game_mode === "Спорт") {
                if (data.message.time_question === 0 && !containsKey(user_id, data.message.your_response) && data.user_id != user_id) {
                    // Поле введите ответ
                    open_answer_popup()
                };
            } else if (room_game_mode === "Совместный ответ") {
                if (data.message.time_question === 0 && !containsKey(user_id, data.message.your_response) && data.user_id != user_id) {
                    // Поле введите ответ
                    console.log("Мы тут", data.message.get_answer)
                    if (data.message.get_answer) {
                        console.log("Мы внутри")
                        if (!data.message.get_answer.type) {
                            open_answer_popup()
                        };
                    };
                };
            };

//            if (data.message.time_question === 0 && data.captain_id === user_id && !checking_popup) {
//                open_answeing()
//            };
            if (clear_chat_check) {
                clear_chat()
            };
            // Скрываем элементы стартовой страницы в пользу элементов новых вопросов
            hide_element()
            // Проверка на ведущего
            if (user_id === data.user_id) {
                hide_access_user()
                showQuestion_leader(data.message)
            } else {
//                document.getElementById('page_question').style.pointerEvents = ""
//                document.getElementById('page').style.pointerEvents = ""
                hide_access_leader()
                showQuestion_user(data.message)
            };

            // Если есть полученный ответ, то останавливаем вопрос и создаём поле ответа
            if (data.message.get_answer) {
//            console.log("Получен ответ", data.message.get_answer);
                if (room_game_mode === "Классика") {
                    pause_question_time()
                    create_answer(data.message.get_answer)
                } else if (room_game_mode === "Спорт") {
                    answer_arr = data.message.get_answer
                    create_answer_arr(answer_arr)

                    let chek_answer_user = true
                    const tuple = data.message.your_response
                    console.log("tuple",tuple)
                    for (let i = 0; i < answer_arr.length; i++) {
                        const key = answer_arr[i].author_answer_id
//                        console.log("key",key)
////                        console.log(tuple)
//                        console.log("tuple[key]",tuple[key])
//                        console.log("containsKey(key, tuple)",containsKey(key, tuple))
                        // Если пользователь ведущий уже оценил ответ пользователя, то данный ответ на отоброжается
                        if (containsKey(key, tuple)) {
                            if (tuple[key]) {
                                document.getElementById(`user_answer_id_${answer_arr[i].author_answer_id}`).style.display = "none";
                            } else {
                                if (chek_answer_user) {
                                    document.getElementById(`user_answer_id_${answer_arr[i].author_answer_id}`).click();
                                    chek_answer_user = false
                                };
                            };
                        }; // data.message.your_response
                    };
                    if (chek_answer_user) {
                        document.getElementById('popup_accepting_answer').style.display = "none";
                    };
                } else if (room_game_mode === "Совместный ответ") {
                    if (user_id === data.captain_id && !data.message.get_answer.type) {
//                        console.log("Это массив")
                        answer_arr = data.message.get_answer
                        create_answer_captain(answer_arr)
                    } else if (user_id === data.user_id && data.message.get_answer.type) {
//                        console.log("Это кортеж")
                        pause_question_time()
                        create_answer(data.message.get_answer)
                    };
                };


            } else {
                console.log("в статусе комнаты нет ответа");
            };
        };
    };
};

const timerElement = document.getElementById('timer');
const write_answer_box_popup = document.getElementById('write_answer_box_popup');
const write_early_response_box_popup = document.getElementById('write_early_response_box_popup');
timerElement.style.display = "none";
write_answer_box_popup.style.display = "none";
write_early_response_box_popup.style.display = "none";

let countdownInterval = null; // Переменная для хранения интервала

function startCountdown(timer_value) {
    console.log("Обратный отсчет перед началом игры запущен");

    // Останавливаем предыдущий таймер, если он был
    if (countdownInterval) {
        clearInterval(countdownInterval);
    };
    show_timer(timer_value)
//    timerElement.textContent = timer_value;
//    let value = parseInt(timerElement.textContent, 10);
    let value = timer_value
    checkScale(timerElement);
//    timerElement.style.display = "";

    countdownInterval = setInterval(() => {
        if (value > 0) {
            value -= 1;
            show_timer(value)
//            timerElement.textContent = value;
        } else {
            clearInterval(countdownInterval);
            timerElement.style.display = "none"; // Скрываем таймер по окончанию
        };
    }, 1000);
};

// Функция для отмены таймера
function cancelCountdown() {
    if (countdownInterval) {
        clearInterval(countdownInterval);
        countdownInterval = null;
        timerElement.style.display = "none";
        console.log("Таймер отменен");
    };
};

function checkScale(event) {
    const width = window.innerWidth;
    const height = window.innerHeight;

    const width_windiw = event.offsetWidth;
    const height_windiw = event.offsetHeight;

    event.style.left = `${Math.floor(width/2)-Math.floor(width_windiw/2)}px`;
    event.style.top = `${Math.floor(height/2)-Math.floor(height_windiw/2)}px`;
};

// Запуск таймера
window.addEventListener('resize', () => checkScale(timerElement));
window.addEventListener('resize', () => checkScale(write_answer_box_popup));
window.addEventListener('resize', () => checkScale(write_early_response_box_popup));