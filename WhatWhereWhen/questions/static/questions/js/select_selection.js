const items_selection = document.getElementById('select_selection_all').querySelectorAll('.select_item');

const select_selection = []


function Timer() {
    if (Time) {
        clearTimeout(Time);
    };
    Time = setTimeout(() => {
        POST(URL_server + URL_adress);
    }, 1000);
}


document.addEventListener('DOMContentLoaded', (event) => {
    items_selection.forEach(item => {

        const checkMarkBox = item.querySelector('.check_mark_box');
        checkMarkBox.querySelector('.select').style.display = 'none';

        item.addEventListener('click', ()=> {
//            console.log(select_selection)
//            Timer()
            let number = item.getAttribute('data-value');
            if (checkMarkBox.querySelector('.select').style.display === 'none') {
                checkMarkBox.querySelector('.select').style.display = '';
                checkMarkBox.querySelector('.base').style.display = 'none';

                if (!select_selection.includes(number)) {
                    select_selection.push(number);
                }

            } else if (checkMarkBox.querySelector('.base').style.display === 'none') {
                checkMarkBox.querySelector('.base').style.display = '';
                checkMarkBox.querySelector('.select').style.display = 'none';

                let index = select_selection.indexOf(number);

                if (index !== -1) {
                    select_selection.splice(index, 1);
                };
            };
        });
    });
});

function filterItemsSelectionAll() {
    console.log("Функция вызвана");
    const input = document.getElementById('select_selection_all_name');
    const filter = input.value.toLowerCase();
    const ul = document.getElementById('spis_select_selection_all');
    const li = ul.getElementsByTagName('li');

    for (let i = 0; i < li.length; i++) {
        const item = li[i].textContent || li[i].innerText;
        if (item.toLowerCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        };
    };
};
