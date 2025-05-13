function showScreen(questionNumber) {
    // Скрываем все вопросы
    const questions = document.querySelectorAll('.appears_text');
    questions.forEach(q => {
        q.style.display = 'none';
    });

    // Сброс цвета всех кнопок
    const buttons = document.querySelectorAll('.question_button'); // Предполагается, что у кнопок есть класс 'question_button'
    buttons.forEach(button => {
        button.style.backgroundColor = "";
//        button.style.borderBottom = "2px solid rgba(136, 128, 136, 1)";
    });

    // Показываем только выбранный вопрос
    let selectedQuestion;
    if (questionNumber === 1) {
        selectedQuestion = document.getElementById("question_box");
        document.getElementById("question_button").style.backgroundColor = "rgba(71, 68, 71, 1)";
//        document.getElementById("question_button").style.borderBottom = "none";
    } else if (questionNumber === 2) {
        selectedQuestion = document.getElementById("note_box");
        document.getElementById("note_button").style.backgroundColor = "rgba(71, 68, 71, 1)";
//        document.getElementById("note_button").style.borderBottom = "none";
    } else if (questionNumber === 3) {
        selectedQuestion = document.getElementById("answer_box");
        document.getElementById("answer_button").style.backgroundColor = "rgba(71, 68, 71, 1)";
//        document.getElementById("answer_button").style.borderBottom = "none";
    };

    if (selectedQuestion) {
        selectedQuestion.style.display = 'block';
    };
};

// Показываем первый вопрос при загрузке страницы



const submit = document.querySelector('#submit_button');
const questionName = document.querySelector('#question_name');
const textQuestion = document.querySelector('#text_question');
const answer = document.querySelector('#answer');

// Функция для проверки заполненности полей
function checkInputs() {
    const questionName = document.querySelector('#question_name');
    const textQuestion = document.querySelector('#text_question');
    const answer = document.querySelector('#answer');

    if (questionName.value && textQuestion.value && answer.value) {
        submit.style.pointerEvents = "";
        submit.style.backgroundColor = "#C0A610";
    } else {
        submit.style.pointerEvents = "none";
        submit.style.backgroundColor = "#393730";
    }
}


// Добавляем обработчик событий для каждого поля ввода
questionName.addEventListener('input', checkInputs);
textQuestion.addEventListener('input', checkInputs);
answer.addEventListener('input', checkInputs);


submit.addEventListener('click', function() {
    document.getElementById('submit').click();
});

submit.addEventListener('mouseover', function() {
    submit.style.backgroundColor = "#524F52";
});


document.addEventListener("DOMContentLoaded", function() {
    // Показываем первый вопрос при загрузке страницы
    showScreen(1);

    // Изначально отключаем кнопку
    submit.style.pointerEvents = "";
    submit.style.backgroundColor = "#C0A610";

    // Проверяем заполненность полей сразу после загрузки
    checkInputs();
});
