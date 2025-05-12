//const Button_Create = document.querySelector('#create_tag');
//
//if (Button_Create) {
//    Button_Create.addEventListener('click', () => {;
//        const dialog = document.createElement('dialog');
//        dialog.classList.add('dialog');
//        dialog.id = 'dialog_create';
//
//        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
//
//        dialog.innerHTML = `
//              <div id="close_dialog_create" class="dialog_close">Закрыть</div>
//              <form method="post" class="forms" id="form_tags_add">
//                  <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
//                  <input id="field_tag" type="text" placeholder="Введите Название тега" class="input_dialog">
//                  <input id="field_tag" type="submit" class="dialog_button" value="Отправить">
//
//              </form>
//            `;
//
//        document.body.appendChild(dialog);
//
//        dialog.showModal();
//
//        close.onclick = function () {
//            dialog.close();
//        };
//    });
//};

const Button_Create = document.querySelector('#create_tag');

if (Button_Create) {
    Button_Create.addEventListener('click', () => {
        const dialog = document.createElement('dialog');
        dialog.classList.add('dialog');
        dialog.id = 'dialog_create';

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        dialog.innerHTML = `
            <form method="post" class="forms" id="form_tags_add">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                <div id="close_dialog_create" class="dialog_close">Закрыть</div>
                <input id="field_tag" type="text" placeholder="Введите Название тега" class="input_dialog">
                <input type="submit" class="dialog_button" value="Отправить">
            </form>
        `;

        document.body.appendChild(dialog);
        dialog.showModal();

        const close = dialog.querySelector('#close_dialog_create');
        close.onclick = function () {
            dialog.close();
        };
    });
};




//// Создаем элемент
//const myElement = document.createElement('div');
//
//// Добавляем id к элементу
//myElement.id = 'myUniqueId';
//
//// Добавляем содержимое в элемент
//myElement.textContent = 'Это элемент с уникальным ID.';
//
//// Добавляем элемент в body
//document.body.appendChild(myElement);


//    parentElement.appendChild(childElement);
//
//    dialog.innerHTML = `
//      <form method="dialog">
//        <dialog>
//        <button type="submit">Закрыть</button>
//      </form>
//    `;
//
//
//
//    Button_Create.addEventListener('click', () => {
//        Dialog.showModal();
//
//        Close_Dialog.onclick = function () {
//            Dialog.close();
//        };
//    });
//}
//
//// Создаем элемент <dialog>
//
//
//// Добавляем содержимое в диалог
//dialog.innerHTML = `
//  <form method="dialog">
//    <p>Это пример диалогового окна.</p>
//    <button type="submit">Закрыть</button>
//  </form>
//`;
//
//// Добавляем диалог в body
//document.body.appendChild(dialog);
//
//// Открываем диалог
//dialog.showModal();
