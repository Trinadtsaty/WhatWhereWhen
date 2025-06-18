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
        if (data.class === "time_question") {
            console.log("время вопроса а не чтения")
        };
    };

    if (data.type === "start_timer") {
        startCountdown(data.message);
    };

    if (data.type === "cancellation") {
        cancelCountdown()
    };

    if (data.type === "question_menu") {
        console.log("мы перед скрытием элемента")
        document.getElementById("question_page").style.display = "none"
        document.getElementById("page").style.display = "none"
        console.log("мы после скрытием элемента")
        if (user_id === data.user_id) {
            hide_element()
            createQuestionMenu(data.message)
        };
    };

    if (data.type === "get_question") {
        hide_element()
        if (user_id === data.user_id) {
            showQuestion_leader(data)
        } else {
            hide_access_leader()
            showQuestion_user(data)
        };
    };
    if (data.type === "status_room") {
        if (data.stage === "collecting") {
            // Вышел за хлебом
            console.log("Вышел за хлебом")
            showe_element()
        } else if (data.stage === "question_menu") {
            if (user_id === data.user_id) {
                hide_element()
                createQuestionMenu(data.message)
            } else {
                hide_all()
            };
        } else if (data.stage === "get_question") {
            hide_element()
            if (user_id === data.user_id) {
                showQuestion_leader(data.message)
            } else {
                hide_access_leader()
                showQuestion_user(data.message)
            };
        };
    };
};

const timerElement = document.getElementById('timer');
timerElement.style.display = "none";
let countdownInterval = null; // Переменная для хранения интервала

function startCountdown(timer_value) {
    console.log("таймер запущен");

    // Останавливаем предыдущий таймер, если он был
    if (countdownInterval) {
        clearInterval(countdownInterval);
    }

    timerElement.textContent = timer_value;
    let value = parseInt(timerElement.textContent, 10);
    checkScale();
    timerElement.style.display = "";

    countdownInterval = setInterval(() => {
        if (value > 0) {
            value -= 1;
            timerElement.textContent = value;
        } else {
            clearInterval(countdownInterval);
            timerElement.style.display = "none"; // Скрываем таймер по окончанию
//            hide_element()
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

function checkScale() {
    const width = window.innerWidth;
    const height = window.innerHeight;

    const width_windiw = timerElement.offsetWidth;
    const height_windiw = timerElement.offsetHeight;

    timerElement.style.left = `${Math.floor(width/2)-Math.floor(width_windiw/2)}px`
    timerElement.style.top = `${Math.floor(height/2)-Math.floor(height_windiw/2)}px`
}
// Запуск таймера

window.addEventListener('resize', checkScale);

//document.querySelector('#answer_open_box').addEventListener('click', function() {
//    document.querySelector('#popup_answer').classList.toggle('show');
//});