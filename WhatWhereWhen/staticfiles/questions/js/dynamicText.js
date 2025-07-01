
function size_on_length(element) {
    const textLength = element.innerText.length;

    // Пример: уменьшаем размер шрифта, если текст длиннее 50 символов
    if (textLength > 10) {
        element.style.fontSize = '10px'; // Маленький размер шрифта
    } else {
        element.style.fontSize = '30px'; // Большой размер шрифта
    };
};

function size_on_appears_text(appears_text) {
    const width = window.innerWidth;
    appears_text.forEach(text_size => {
        if (width > 1000) {
            text_size.style.fontSize = '40px';

        } else {
            text_size.style.fontSize = '25px';
        };
    });
};

function size_on_tage(correction_text_size) {
    const width = window.innerWidth;
    correction_text_size.forEach(text_size => {
        if (width > 1000) {
            text_size.style.fontSize = '25px';
        } else {
            text_size.style.fontSize = '15px';
        };
    });
};



// Вызываем функцию при загрузке страницы
const correction_text_length = document.querySelectorAll(".dynamic_length");
const correction_text_size = document.querySelectorAll(".dynamic_size");
const appears_text = document.querySelectorAll(".appears_text");



if (correction_text_length.length > 0) {
    correction_text_length.forEach(text => {
        size_on_length(text);
    });
};

if (correction_text_size.length > 0) {
    size_on_tage(correction_text_size)

    // Добавляем обработчик события 'resize'
    window.addEventListener('resize', () => size_on_tage(correction_text_size));
};

if (appears_text.length > 0) {
    size_on_appears_text(appears_text)

    // Добавляем обработчик события 'resize'
    window.addEventListener('resize', () => size_on_appears_text(appears_text));
};


const author_question_size = document.querySelector("#author_login");
const authorTextLength = author_question_size.textContent.length; // Получаем длину текста

console.log(authorTextLength);

if (authorTextLength <= 5) {
    author_question_size.style.fontSize = '50px';
} else if (authorTextLength <= 10) {
    author_question_size.style.fontSize = '25px';
} else if (authorTextLength <= 15) {
    author_question_size.style.fontSize = '16px';
} else if (authorTextLength <= 20) {
    author_question_size.style.fontSize = '12px';
}

const authorBox = document.querySelector("#author_box");

// Получение размеров контейнера
const width = authorBox.clientWidth; // Ширина
const height = authorBox.clientHeight; // Высота

console.log(`Ширина: ${width}px, Высота: ${height}px`);
