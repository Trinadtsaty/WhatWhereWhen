//const URL_server = 'http://127.0.0.1:8000'
//const URL_adress = '/questions/api/v1'



//fetch(URL_server + URL_adress, {
//    method: 'GET', // Указываем метод запроса
//})
//    .then((response) => {
//        // Проверяем, успешен ли ответ
//        if (!response.ok) {
//            throw new Error('Network response was not ok ' + response.statusText);
//        }
//        return response.json(); // Преобразуем ответ в JSON
//    })
//    .then((data) => {
//        console.log(data); // Обработка полученных данных
//    })
//    .catch((error) => {
//        console.error('There was a problem with the fetch operation:', error);
//    });

//const URL_server1 = 'http://127.0.0.1:8000'
//const URL_adress = '/questions/api/v1'
//
//const data = {
//    "question": 1,
//    "estimation": 7
//}


//fetch(URL_server1 + URL_adress, {
//    method: 'PUT',
//    headers: {
//        'Content-Type': 'application/json', // Указываем тип контента
//        'X-CSRFToken': getCookie('csrftoken')
//    },
//    body: JSON.stringify(data),
//})
//    .then((response) => {
//        if (!response.ok) {
//            throw new Error('Network response was not ok ' + response.statusText);
//        }
//        return response.json();
//    })
//    .then((data) => {
//        console.log(data);
//    })
//    .catch((error) => {
//        console.error('There was a problem with the fetch operation:', error);
//    });
//
//
//function getCookie(name) {
//    let cookieValue = null;
//    if (document.cookie && document.cookie !== '') {
//        const cookies = document.cookie.split(';');
//        for (let i = 0; i < cookies.length; i++) {
//            const cookie = cookies[i].trim();
//            // Проверяем, начинается ли cookie с нужного имени
//            if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                break;
//            }
//        }
//    }
//    return cookieValue;
//}




const URL_server = 'http://127.0.0.1:8000'
const URL_adress = '/questions/api/v1'



function POST(data, URL) {
    fetch(URL, {
        method: 'PUT',
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
    })

};
function PUT(data, URL) {
    console.log(URL)
    fetch(URL, {
        method: 'PUT',
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
    })

};

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

//const data = {
//    "question": 1,
//    "estimation": 2
//}

PUT(data, URL_server + URL_adress)
//POST(data, URL_server + URL_adress)
//if (che) {
//
//} else {
//
//};
//che = true;