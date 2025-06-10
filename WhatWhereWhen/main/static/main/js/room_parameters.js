const img_check = document.querySelectorAll(".img_check");

img_check.forEach(item => {
    item.addEventListener('click', () => {
        console.log(item.dataset.value)
        if (item.dataset.value === "True") {

            item.parentElement.querySelector(".False").style.display = "";
            item.parentElement.querySelector(".True").style.display = "none";

            if (item.dataset.type === "close") {
                password.style.display = "none";
                document.getElementById('room_password').value = '';
                document.getElementById("room_close").checked = false;
            } else if (item.dataset.type === "early_answer") {
                document.getElementById("room_time_early_answer_box").style.display = "none";
                document.getElementById("room_early_answer").checked = false;
            } else if (item.dataset.type === "chat_clean") {
                document.getElementById("room_chat_clean").checked = false;
            } else if (item.dataset.type === "show_question") {
                document.getElementById("room_show_question").checked = false;
            } else if (item.dataset.type === "random_order") {
                document.getElementById("room_break_questions_box").style.display = "none";
                document.getElementById("room_random_order").checked = false;
            };
        } else {

            item.parentElement.querySelector(".False").style.display = "none";
            item.parentElement.querySelector(".True").style.display = "";

            if (item.dataset.type === "close") {
                password.style.display = "";
                document.getElementById("room_close").checked = true;
            } else if (item.dataset.type === "early_answer") {
                document.getElementById("room_time_early_answer_box").style.display = "";
                document.getElementById("room_early_answer").checked = true;
            } else if (item.dataset.type === "chat_clean") {
                document.getElementById("room_chat_clean").checked = true;
            } else if (item.dataset.type === "show_question") {
                document.getElementById("room_show_question").checked = true;
            } else if (item.dataset.type === "random_order") {
                document.getElementById("room_break_questions_box").style.display = "";
                document.getElementById("room_random_order").checked = true;
            };
        };
    });
});