const search_box_button = document.getElementById('search_name_box');
const search_advanced_box = document.getElementById('search_advanced_box');
const question_search = document.getElementById('question_search');
const advanced_search_img = document.getElementById('advanced_search_img');

document.addEventListener('DOMContentLoaded', (event) => {
    POST(URL_server + URL_adress);
});

search_advanced_box.style.display = 'none';
document.getElementById('question_search_title').value = "";
document.getElementById('question_search_text').value = "";
document.getElementById('question_search_answer').value = "";
document.getElementById('checkbox_search').checked = "";

search_box_button.addEventListener('click', () => {
    if (search_advanced_box.style.display === 'none') {
        question_search.style.display = 'none';
        question_search.value=""
        advanced_search_img.style.transform = 'rotate(180deg)';
        search_advanced_box.style.display = '';

        Timer()
    } else {
        question_search.style.display = '';
        advanced_search_img.style.transform = 'rotate(0deg)';
        search_advanced_box.style.display = 'none';
        document.getElementById('question_search_title').value = "";
        document.getElementById('question_search_text').value = "";
        document.getElementById('question_search_answer').value = "";
        document.getElementById('checkbox_search').checked = "";

        Timer()
    }
});

const tags_box = document.getElementById('select_tags');
const tags_search_img = document.getElementById('tags_search_img');
const tags_name_button = document.getElementById('tags_name_box');

tags_box.style.display = 'none';

tags_name_button.addEventListener('click', () => {
    if (tags_box.style.display === 'none') {

        tags_search_img.style.transform = 'rotate(180deg)';
        tags_box.style.display = '';
    } else {
        tags_box.style.display = 'none';
        tags_search_img.style.transform = 'rotate(0deg)';

        document.querySelectorAll('.select_item_tags').forEach(item => {
            item.querySelector('.check_mark_box').querySelector('.select').style.display = 'none';
            item.querySelector('.check_mark_box').querySelector('.unselect').style.display = 'none';
            item.querySelector('.check_mark_box').querySelector('.base').style.display = '';
        });

        select_tag.length = 0;
        unselect_tag.length = 0;

        Timer()
    }
});

const select_author_menu = document.getElementById('select_author');
const author_search_img = document.getElementById('author_search_img');
const author_name_button = document.getElementById('author_name_box');

select_author_menu.style.display = 'none';

author_name_button.addEventListener('click', () => {
    if (select_author_menu.style.display === 'none') {

        author_search_img.style.transform = 'rotate(180deg)';
        select_author_menu.style.display = '';
    } else {
        select_author_menu.style.display = 'none';
        tags_search_img.style.transform = 'rotate(0deg)';

        document.querySelectorAll('.select_item_author').forEach(item => {
            item.querySelector('.check_mark_box').querySelector('.select').style.display = 'none';
            item.querySelector('.check_mark_box').querySelector('.unselect').style.display = 'none';
            item.querySelector('.check_mark_box').querySelector('.base').style.display = '';
        });

        select_author.length = 0;
        unselect_author.length = 0;

        Timer()
    }
});



function formatQuestionText(text) {
    // Заменяем переносы на пробелы
    text = text.replace(/\n/g, ' ');
    // Если длина текста больше 20 символов, обрезаем и добавляем "..."
    return text.length > 20 ? text.slice(0, 20) + '...' : text;
};


function POST(URL) {
        const search = document.getElementById('question_search').value;
        const search_name = document.getElementById('question_search_title').value;
        const search_text = document.getElementById('question_search_text').value;
        const search_answer = document.getElementById('question_search_answer').value;

        const coincidence_tag = document.getElementById('checkbox_tag').checked

        const question_page = 0
        const count_question = document.getElementById('count_question').value
        const sorting_question = document.getElementById('sorting_question').value

        const checkbox_search = document.getElementById('checkbox_search').checked

        const data = {
            "search": search,
            "search_name": search_name,
            "search_text": search_text,
            "search_answer": search_answer,
            "checkbox_search":checkbox_search,
            "coincidence_tag":coincidence_tag,
            "select_author": select_author,
            "unselect_author":unselect_author,
            "select_tag":select_tag,
            "unselect_tag":unselect_tag,
            "question_page": question_page,
            "count_question": count_question,
            "sorting_question":sorting_question,
        };

    return fetch(URL, {
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
        return response.json(); // Возвращаем ответ в формате JSON
    })
    .then(data => {
        console.log(data); // Логируем ответ для отладки

        // Вы можете также получить доступ к другим данным:
        console.log(data.questions); // Данные, которые вы передали через JsonResponse
//        console.log(data.questions[0].question_name)
        const questions_box = document.getElementById('question_scroll_box');

        //Очищаем элемент
        while (questions_box.firstChild) {
            questions_box.removeChild(questions_box.firstChild);
        }

        const array_element = data.questions

        //Отоброжение отсортированного массива на странице

        for (const question of array_element) {

//            console.log(question.question_name, question.question_text)
            const QuestionName = document.createElement('div');
            QuestionName.className = 'name_question';
            QuestionName.textContent=question.question_name;

            const QuestionText = document.createElement('div');
            QuestionText.className = 'text_question';
            QuestionText.textContent=formatQuestionText(question.text_question);

            const Estimation = document.createElement('div');
            Estimation.className = 'estimation';
            Estimation.textContent=question.average_estimation;

            const textbox = document.createElement('div');
            textbox.className = 'box_text';
            textbox.appendChild(QuestionName)
            textbox.appendChild(QuestionText)

            const EstimationQuestion = document.createElement('div');
            EstimationQuestion.className = 'question_estimation';
            EstimationQuestion.appendChild(Estimation)

            const newlink  = document.createElement('a');
            newlink.className = 'link_question_page';
            newlink.href=`/questions/${question.ID}/`;
            newlink.appendChild(textbox)
            newlink.appendChild(EstimationQuestion)

            const button = document.createElement('div');
            button.className = 'button_tools';
            button.textContent = '|||';

            const li_element_add = document.createElement('li');
            li_element_add.className = 'tools_element';
            li_element_add.textContent = 'Добавить в коллекцию';

            const a_link = document.createElement('a');
            a_link.className = 'a_link';
            a_link.href=`/questionclaim/${question.ID}/`
            a_link.textContent = 'Пожаловаться'

            const li_element_claim = document.createElement('li');
            li_element_claim.className = 'tools_element';
            li_element_claim.appendChild(a_link)

            const ul_spis = document.createElement('ul');
            ul_spis.className = 'tools_menu';
            ul_spis.appendChild(li_element_add)
            ul_spis.appendChild(li_element_claim)

            const newbox = document.createElement('div');
            newbox.className = 'link_box_question';
            newbox.appendChild(newlink)
            newbox.appendChild(button)
            newbox.appendChild(ul_spis)

            questions_box.appendChild(newbox)
        };

    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
};
window.POST = POST;




const URL_server = 'http://127.0.0.1:8000';
const URL_adress = '/questions/';



// Обработчики событий для полей input
question_search.addEventListener('input', () => {
    const search = question_search.value;
    if (search) {
        Timer()
    }
});

document.getElementById('question_search_title').addEventListener('input', () => {
    const search_name = document.getElementById('question_search_title').value;
    if (search_name) {
        Timer()
    }
});

document.getElementById('question_search_text').addEventListener('input', () => {
    const search_text = document.getElementById('question_search_text').value;
    if (search_text) {
        Timer()
    }
});

document.getElementById('question_search_answer').addEventListener('input', () => {
    const search_answer = document.getElementById('question_search_answer').value;
    if (search_answer) {
        Timer()
    }
});

// Обработчики событий для полей select
document.getElementById('count_question').addEventListener('change', () => {
    const count_question = document.getElementById('count_question').value;
    if (count_question) {
        Timer()
    }
});

document.getElementById('sorting_question').addEventListener('change', () => {
    const sorting_question = document.getElementById('sorting_question').value;
    if (sorting_question) {
        Timer()
    }
});

document.getElementById('checkbox_search').addEventListener('change', () => {
    const checkbox_search = document.getElementById('checkbox_search').checked;
    if (checkbox_search) {
        Timer()
    }
});

document.getElementById('checkbox_tag').addEventListener('change', () => {
    const checkbox_tag = document.getElementById('checkbox_tag').checked;
    if (checkbox_tag) {
        Timer()
    }
});

