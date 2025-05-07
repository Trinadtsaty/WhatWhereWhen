document.querySelectorAll('.achievement').forEach(item => {
    item.addEventListener('click', function() {

        const title = this.getAttribute('data-title');
        const time = this.getAttribute('data-titleTime');

        const Dialog_achievement_description = document.querySelector("#achievement_description");
        const close = document.querySelector("#close");
        const Description_Box = document.querySelector("#description_box");
        const Time_Box = document.querySelector("#time_box");

        while (Description_Box.firstChild) {
            Description_Box.removeChild(Description_Box.firstChild);
        }

        Description_Box.textContent = title;
        Time_Box.textContent = time;

        Dialog_achievement_description.showModal();
        close.onclick = function () {
            Dialog_achievement_description.close();
        };

    });
});

