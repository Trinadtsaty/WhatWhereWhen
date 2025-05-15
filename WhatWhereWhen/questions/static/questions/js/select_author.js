const items_author = document.getElementById('select_author').querySelectorAll('.select_item');

const select_author = []
const unselect_author = []

function Timer() {
    if (Time) {
        clearTimeout(Time);
    };
    Time = setTimeout(() => {
        POST(URL_server + URL_adress);
    }, 5000);
}


document.addEventListener('DOMContentLoaded', (event) => {
    items_author.forEach(item => {

        const checkMarkBox = item.querySelector('.check_mark_box');
        checkMarkBox.querySelector('.select').style.display = 'none';
        checkMarkBox.querySelector('.unselect').style.display = 'none';

        item.addEventListener('click', ()=> {
            Timer()
            let number = item.getAttribute('data-value');
            if (checkMarkBox.querySelector('.select').style.display === 'none' && checkMarkBox.querySelector('.unselect').style.display === 'none') {
                checkMarkBox.querySelector('.select').style.display = '';
                checkMarkBox.querySelector('.base').style.display = 'none';

                if (!select_author.includes(number)) {
                    select_author.push(number);
                }

            } else if (checkMarkBox.querySelector('.base').style.display === 'none' && checkMarkBox.querySelector('.unselect').style.display === 'none') {
                checkMarkBox.querySelector('.unselect').style.display = '';
                checkMarkBox.querySelector('.select').style.display = 'none';

                let index = select_author.indexOf(number);

                if (index !== -1) {
                    select_author.splice(index, 1);
                };

                if (!unselect_author.includes(number)) {
                    unselect_author.push(number);
                };

            } else if (checkMarkBox.querySelector('.base').style.display === 'none' && checkMarkBox.querySelector('.select').style.display === 'none') {
                checkMarkBox.querySelector('.base').style.display = '';
                checkMarkBox.querySelector('.unselect').style.display = 'none';

                let index = unselect_author.indexOf(number);

                if (index !== -1) {
                    unselect_author.splice(index, 1);
                };
            };
        });
    });
});

function filterItemsAuthor() {
    const input = document.getElementById('select_author_name');
    const filter = input.value.toLowerCase();
    const ul = document.getElementById('spis_select_author');
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
