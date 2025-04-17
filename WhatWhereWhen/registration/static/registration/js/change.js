const Change_buttons = document.querySelectorAll('.change');
const Change_dialog = document.querySelector("#change_nick_photo");
const Change_dialog_form = document.querySelector("#change_photo_nick");

function previewImage() {
//    const file = document.getElementById('image_change').files[0];
    const file = document.getElementById('Image_User').files[0];
    const img = document.getElementById('IMG_change');

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            img.src = e.target.result; // Устанавливаем источник изображения
        }
        reader.readAsDataURL(file); // Читаем файл как URL
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('Image_User').addEventListener('change', previewImage);
});

image = document.querySelector("#image_change");
image.addEventListener('click', function() {
    document.getElementById('Image_User').click();
});

Change_buttons.forEach(Change_button => {
    Change_button.addEventListener('click', () => {
        Change_dialog.showModal();

        close = document.querySelector("#Back");
        Continue = document.querySelector("#Continue");

        Continue.onclick = function () {
            document.getElementById('register_button').click();
            Change_dialog.close();
            Change_dialog_form.reset();
        };

        close.onclick = function () {
            Change_dialog.close();
            Change_dialog_form.reset();
        };
    });
});
