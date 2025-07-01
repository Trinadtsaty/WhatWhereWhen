
function showQuestion(questionNumber) {
    // Скрываем все вопросы
    const questions = document.querySelectorAll('.appears_text');
    questions.forEach(q => {
        q.style.display = 'none';
    });

    // Сброс цвета всех кнопок
    const buttons = document.querySelectorAll('.question_button'); // Предполагается, что у кнопок есть класс 'question_button'
    buttons.forEach(button => {
        button.style.backgroundColor = "";
        button.style.borderBottom = "2px solid rgba(82, 79, 82, 1)";
    });

    // Показываем только выбранный вопрос
    let selectedQuestion;
    if (questionNumber === 1) {
        selectedQuestion = document.getElementById("question");
        document.getElementById("question_button").style.backgroundColor = "rgba(136, 128, 136, 1)";
        document.getElementById("question_button").style.borderBottom = "none";
    } else if (questionNumber === 2) {
        selectedQuestion = document.getElementById("note");
        document.getElementById("note_button").style.backgroundColor = "rgba(136, 128, 136, 1)";
        document.getElementById("note_button").style.borderBottom = "none";
    } else if (questionNumber === 3) {
        selectedQuestion = document.getElementById("answer");
        document.getElementById("answer_button").style.backgroundColor = "rgba(136, 128, 136, 1)";
        document.getElementById("answer_button").style.borderBottom = "none";
    } else if (questionNumber === 4) {
        selectedQuestion = document.getElementById("license");
        document.getElementById("license_button").style.backgroundColor = "rgba(136, 128, 136, 1)";
        document.getElementById("license_button").style.borderBottom = "none";
    };

    if (selectedQuestion) {
        selectedQuestion.style.display = 'block';
    };
};

// Показываем первый вопрос при загрузке страницы
window.onload = function() {
    showQuestion(1);
};

