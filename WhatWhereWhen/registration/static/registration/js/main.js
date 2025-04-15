console.log('123')


document.querySelectorAll('.achievement').forEach(item => {
    item.addEventListener('click', function() {

        const title = this.getAttribute('data-title');

        const Dialog_achievement_description = document.querySelector("#achievement_description");
        const close = document.querySelector("#close");
        const Description_Box = document.querySelector("#description_box");

        while (Description_Box.firstChild) {
            Description_Box.removeChild(Description_Box.firstChild);
        }

        Description_Box.textContent = title;

        Dialog_achievement_description.showModal();
        close.onclick = function () {
            Dialog_achievement_description.close();
        };

    });
});

