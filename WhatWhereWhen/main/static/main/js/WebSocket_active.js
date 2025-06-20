//document.addEventListener('DOMContentLoaded', function() {
const activeSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/active/' + room_number + '/'
);
activeSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);

    if (data.type === "time") {
        time_output(data.time)
        if (data.Class === "time_question" && user_id != data.leader_id) {
            show_access_user()
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
            document.getElementById('show_messege_people').textContent = data.status;
            document.getElementById('show_messege_people').className = data.Class;
            show("show_messege_people")
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
        create_answer(data)
        pause_question_time()
    };
    if (data.type === "random_question") {
        activeSocket.send(JSON.stringify({
            'question': data.question_number,
            'type' : "open_question",
        }));
    };

    if (data.type === "get_question") {
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
        } else if (data.message.your_response === user_id) {
            open_answer_popup()
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
            if (clear_chat_check) {
                clear_chat()
            };
            hide_element()
            if (user_id === data.user_id) {
                hide_access_user()
                showQuestion_leader(data.message)
            } else {
//                document.getElementById('page_question').style.pointerEvents = ""
//                document.getElementById('page').style.pointerEvents = ""
                hide_access_leader()
                showQuestion_user(data.message)
            };
            if (data.message.get_answer) {
                pause_question_time()
                create_answer(data.message.get_answer)
                console.log(data.message.get_answer);
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
    console.log("таймер запущен");

    // Останавливаем предыдущий таймер, если он был
    if (countdownInterval) {
        clearInterval(countdownInterval);
    }

    timerElement.textContent = timer_value;
    let value = parseInt(timerElement.textContent, 10);
    checkScale(timerElement);
    timerElement.style.display = "";

    countdownInterval = setInterval(() => {
        if (value > 0) {
            value -= 1;
            timerElement.textContent = value;
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


