//const question = document.querySelectorAll('.link_box_question');
//
////const URL_server = 'http://127.0.0.1:8000';
//const URL_Selection = 'api/v3';


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

function POST_Selection(data, URL) {
    fetch(URL, {
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
    })
};



//question.forEach(item => {
//    const button_selection = item.querySelector('.selection');
//    const number = item.getAttribute('data-value');
//    button_selection.addEventListener('click', ()=> {
//        console.log(number)
//    });
//});