const URL_server = 'http://127.0.0.1:8000'
console.log(URL_server + '/questions/api/v1/')


fetch(URL_server + '/questions/api/v1', {
    method: 'GET', // Указываем метод запроса
})
    .then((response) => {
        // Проверяем, успешен ли ответ
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json(); // Преобразуем ответ в JSON
    })
    .then((data) => {
        console.log(data); // Обработка полученных данных
    })
    .catch((error) => {
        console.error('There was a problem with the fetch operation:', error);
    });



const data = {
    'titles_name' : "Оценка",
    'titles_description': 3,
}

fetch(URL_server + '/questions/api/v1', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json', // Указываем тип контента
    },
    body: JSON.stringify(data),
})
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then((data) => {
        console.log(data);
    })
    .catch((error) => {
        console.error('There was a problem with the fetch operation:', error);
    });

