
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
        button.style.borderBottom = "2px solid rgba(136, 128, 136, 1)";
    });

    // Показываем только выбранный вопрос
    let selectedQuestion;
    if (questionNumber === 1) {
        selectedQuestion = document.getElementById("question_box");
        document.getElementById("question_button").style.backgroundColor = "rgba(71, 68, 71, 1)";
        document.getElementById("question_button").style.borderBottom = "none";
    } else if (questionNumber === 2) {
        selectedQuestion = document.getElementById("note_box");
        document.getElementById("note_button").style.backgroundColor = "rgba(71, 68, 71, 1)";
        document.getElementById("note_button").style.borderBottom = "none";
    } else if (questionNumber === 3) {
        selectedQuestion = document.getElementById("answer_box");
        document.getElementById("answer_button").style.backgroundColor = "rgba(71, 68, 71, 1)";
        document.getElementById("answer_button").style.borderBottom = "none";
    };

    if (selectedQuestion) {
        selectedQuestion.style.display = 'block';
    };
};

// Показываем первый вопрос при загрузке страницы
window.onload = function() {
    showScreen(1);
};


const submit = document.querySelector('#submit_button');

submit.addEventListener('click', function() {
    console.log(123)
});
