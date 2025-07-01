


function adjustFontSize() {
            const textLength = element.innerText.length;

            // Пример: уменьшаем размер шрифта, если текст длиннее 50 символов
            if (textLength > 10) {
                element.style.fontSize = '16px'; // Маленький размер шрифта
            } else {
                element.style.fontSize = '32px'; // Большой размер шрифта
            }
        }

        // Вызываем функцию при загрузке страницы
const element = document.querySelector(".dynamic-text");

if (element) {
    adjustFontSize();
};
