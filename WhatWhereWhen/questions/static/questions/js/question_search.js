function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем, начинается ли cookie с нужного имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function POST(data, URL) {
    return fetch(URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // Указываем тип контента
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json(); // Возвращаем ответ в формате JSON
    });
};



const test_POST = document.querySelector('#test_post');

const URL_server = 'http://127.0.0.1:8000';
const URL_adress = '/questions/';

if (test_POST) {
    const test = {
        "test": test_POST.value // Получаем значение поля ввода
    };
    POST(test, URL_server + URL_adress)
        .then(data => {
            console.log(data); // Логируем ответ для отладки
            alert(data.message); // Например, показываем сообщение
            // Вы можете также получить доступ к другим данным:
            console.log(data.data); // Данные, которые вы передали через JsonResponse
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
}

