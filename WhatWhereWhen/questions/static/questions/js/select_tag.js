const items_tags = document.getElementById('select_tags').querySelectorAll('.select_item');

const select_tag = []
const unselect_tag = []

let Time;

function Timer() {
    console.log("Timer Start")
    if (Time) {
        clearTimeout(Time);
    };
    Time = setTimeout(() => {
        POST(URL_server + URL_adress);
    }, 5000);
}


document.addEventListener('DOMContentLoaded', (event) => {
    // Скрываем все изображения в других элементах
    items_tags.forEach(item => {
        const checkMarkBox = item.querySelector('.check_mark_box');
        checkMarkBox.querySelector('.select').style.display = 'none';
        checkMarkBox.querySelector('.unselect').style.display = 'none';

        item.addEventListener('click', ()=> {
            Timer()
            let number = item.getAttribute('data-value');
            if (checkMarkBox.querySelector('.select').style.display === 'none' && checkMarkBox.querySelector('.unselect').style.display === 'none') {
                checkMarkBox.querySelector('.select').style.display = '';
                checkMarkBox.querySelector('.base').style.display = 'none';

                if (!select_tag.includes(number)) {
                    select_tag.push(number);
                }

            } else if (checkMarkBox.querySelector('.base').style.display === 'none' && checkMarkBox.querySelector('.unselect').style.display === 'none') {
                checkMarkBox.querySelector('.unselect').style.display = '';
                checkMarkBox.querySelector('.select').style.display = 'none';

                let index = select_tag.indexOf(number);

                if (index !== -1) {
                    select_tag.splice(index, 1);
                };

                if (!unselect_tag.includes(number)) {
                    unselect_tag.push(number);
                };

            } else if (checkMarkBox.querySelector('.base').style.display === 'none' && checkMarkBox.querySelector('.select').style.display === 'none') {
                checkMarkBox.querySelector('.base').style.display = '';
                checkMarkBox.querySelector('.unselect').style.display = 'none';

                let index = unselect_tag.indexOf(number);

                if (index !== -1) {
                    unselect_tag.splice(index, 1);
                };
            };
        });
    });
});



function filterItemsTags() {
    const input = document.getElementById('select_tags_name');
    const filter = input.value.toLowerCase();
    const ul = document.getElementById('spis_select_tags');
    const li = ul.getElementsByTagName('li');

    for (let i = 0; i < li.length; i++) {
        const item = li[i].textContent || li[i].innerText;
        if (item.toLowerCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
