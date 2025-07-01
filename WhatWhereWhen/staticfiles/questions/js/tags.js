const Dialog = document.querySelector('#dialog_tegs_all');
const Button_tegs = document.querySelector('#add_teg');
const Close_Dialog = document.querySelector('#close_dialog');
const URL_adress2 = '/questions/api/v2'

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
if (Button_tegs) {
    Button_tegs.addEventListener('click', () => {
        Dialog.showModal();

        const Tags = document.querySelectorAll('.all_tag');
        Tags.forEach(Tag => {
            Tag.addEventListener('click', () => {
                const data = {
                    "tags_id": Tag.getAttribute('data-value'),
                    "question_id": question_number
                };
                POST(data, URL_server + URL_adress2)

                setTimeout(function() {
                    location.reload(); // Перезагружает страницу через 1 секунду (1000 миллисекунд)
                }, 500); // 1000 миллисекунд = 1 секунда
            });
        });

        Close_Dialog.onclick = function () {
            Dialog.close();
        };
    });
}




function filterItems() {
    const input = document.getElementById('text_input');
    const filter = input.value.toLowerCase();
    const ul = document.getElementById('all_tags');
    const li = document.querySelectorAll('.all_tag');

    for (let i = 0; i < li.length; i++) {
        const item = li[i].textContent || li[i].innerText;
        if (item.toLowerCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}