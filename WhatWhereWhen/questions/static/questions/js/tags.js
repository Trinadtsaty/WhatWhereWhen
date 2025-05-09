console.log(123)

const Dialog = document.querySelector('#dialog_tegs_all');
const Button_tegs = document.querySelector('#add_teg');
const Сlose_Dialog = document.querySelector('#close_dialog');

Button_tegs.addEventListener('click', () => {
    Dialog.showModal();
});

//Сlose_Dialog.addEventListener('click', () => {
//    Dialog.close();
//});


Сlose_Dialog.onclick = function () {
    Dialog.close();
};