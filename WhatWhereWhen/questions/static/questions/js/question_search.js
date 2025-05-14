const search_box_button = document.getElementById('search_name_box');
const search_advanced_box = document.getElementById('search_advanced_box');
const question_search = document.getElementById('question_search');
const advanced_search_img = document.getElementById('advanced_search_img');

const search = document.getElementById('question_search').value;
const search_name = document.getElementById('question_search_title').value;
const search_text = document.getElementById('question_search_text').value;
const search_answer = document.getElementById('question_search_answer').value;

const coincidence_tag = document.getElementById('checkbox_tag').checked

const question_page = 0
const count_question = 5

const data = {
    "search": search,
    "search_name": search_name,
    "search_text": search_text,
    "search_answer": search_answer,
    "coincidence_tag":coincidence_tag,
    "select_author":select_author,
    "unselect_author":unselect_author,
    "select_tag":select_tag,
    "unselect_tag":unselect_tag,
    "question_page": question_page,
    "count_question": count_question,
};



search_advanced_box.style.display = 'none';

search_box_button.addEventListener('click', () => {
    if (search_advanced_box.style.display === 'none') {
        question_search.style.display = 'none';
        advanced_search_img.style.transform = 'rotate(180deg)';
        search_advanced_box.style.display = '';
    } else {
        question_search.style.display = '';
        advanced_search_img.style.transform = 'rotate(0deg)';
        search_advanced_box.style.display = 'none';
    }
});



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



const submit_search = document.querySelector('#submit_search');

const URL_server = 'http://127.0.0.1:8000';
const URL_adress = '/questions/';

submit_search.addEventListener('click', ()=> {
    if (data) {
        POST(data, URL_server + URL_adress)
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
});

//const div = document.getElementById('search_name_box');
//const width = div.offsetWidth;
//const height = div.offsetHeight;
//
//console.log(`Ширина: ${width}px, Высота: ${height}px`);