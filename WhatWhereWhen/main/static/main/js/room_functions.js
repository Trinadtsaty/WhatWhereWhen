if (document.getElementById("question_page")) {
    const setting_page = document.getElementById("settings_page")
    const player_page = document.getElementById("players_page")
    const question_page = document.getElementById("question_page")
    const button_show_settings = document.getElementById("settings")
    const button_show_question = document.getElementById("question_button")

    button_show_question.addEventListener('click', () => {
        if (question_page.style.display === "none" && player_page.style.display === "") {
            question_page.style.display = ""
            player_page.style.display = "none"
            button_show_question.textContent = "Игроки"
        } else if (question_page.style.display === "none" && player_page.style.display === "none" && setting_page.style.display === "") {
            question_page.style.display = ""
            setting_page.style.display = "none"
            button_show_question.textContent = "Игроки"
            button_show_settings.textContent = "Параметры"
        } else if (question_page.style.display === "") {
            question_page.style.display = "none"
            player_page.style.display = ""
            button_show_question.textContent = "Вопросы"
        };
    });

    button_show_settings.addEventListener('click', () => {
        if (setting_page.style.display === "none" && player_page.style.display === "") {
            setting_page.style.display = ""
            player_page.style.display = "none"
            button_show_settings.textContent = "Игроки"
        } else if (setting_page.style.display === "none" && player_page.style.display === "none" && question_page.style.display === "") {
            question_page.style.display = "none"
            setting_page.style.display = ""
            button_show_settings.textContent = "Игроки"
            button_show_question.textContent = "Вопросы"
        } else if (setting_page.style.display === "") {
            setting_page.style.display = "none"
            player_page.style.display = ""
            button_show_settings.textContent = "Параметры"
        };
    });

} else {
    const setting_page = document.getElementById("settings_page")
    const player_page = document.getElementById("players_page")
    const button_show_settings = document.getElementById("settings")

    button_show_settings.addEventListener('click', () => {
        if (setting_page.style.display === "none") {
            setting_page.style.display = ""
            player_page.style.display = "none"
            button_show_settings.textContent = "Игроки"
        } else if (player_page.style.display === "none") {
            player_page.style.display = ""
            setting_page.style.display = "none"
            button_show_settings.textContent = "Параметры"
        };
    });
};



