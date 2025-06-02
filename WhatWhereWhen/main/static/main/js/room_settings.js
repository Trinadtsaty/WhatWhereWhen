const password_check = document.getElementById("room_close");
const password = document.getElementById("room_password_box");
if (password_check.checked) {
    password.style.display = "";
} else {
    password.style.display = "none";
};
password_check.addEventListener('click', () => {
    if (password_check.checked) {
        password.style.display = "";
    } else {
        password.style.display = "none";
    };
});

const early_answer_check = document.getElementById("room_early_answer");
const time_early_answer = document.getElementById("room_time_early_answer_box");

if (early_answer_check.checked) {
    time_early_answer.style.display = "";
} else {
    time_early_answer.style.display = "none";
};

early_answer_check.addEventListener('click', () => {
    if (early_answer_check.checked) {
        time_early_answer.style.display = "";
    } else {
        time_early_answer.style.display = "none";
    };
});

const random_order = document.getElementById("room_random_order");
const break_questions = document.getElementById("room_break_questions_box");

if (random_order.checked) {
    break_questions.style.display = "";
} else {
    break_questions.style.display = "none";
};

random_order.addEventListener('click', () => {
    if (random_order.checked) {
        break_questions.style.display = "";
    } else {
        break_questions.style.display = "none";
    };
});

const people_limit = document.getElementById('room_people_limit');
const people_limit_return = document.getElementById('slider_return');

// Обновляем отображаемое значение при перемещении ползунка
people_limit.addEventListener('input', function() {
    people_limit_return.textContent = people_limit.value;
});

function filterItemsSelection() {
    const input = document.getElementById('select_Selections_name');
    const filter = input.value.toLowerCase();
    const ul = document.getElementById('spis_selections');
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
const Roles = document.getElementById('popup_roles');
const Selections = document.getElementById('popup_selections');
const Modes = document.getElementById('popup_modes');

function checkScaleRoles() {
    const width = window.innerWidth;
    const height = window.innerHeight;

    const width_windiw = Roles.offsetWidth;
    const height_windiw = Roles.offsetHeight;

    Roles.style.left = `${Math.floor(width/2)-Math.floor(width_windiw/2)}px`
    Roles.style.top = `${Math.floor(height/2)-Math.floor(height_windiw/2)}px`
}
function closePopupRoles() {
    Roles.style.display = "none";
};

function checkScaleSelections() {
    const width = window.innerWidth;
    const height = window.innerHeight;

    const width_windiw = Selections.offsetWidth;
    const height_windiw = Selections.offsetHeight;

    Selections.style.left = `${Math.floor(width/2)-Math.floor(width_windiw/2)}px`
    Selections.style.top = `${Math.floor(height/2)-Math.floor(height_windiw/2)}px`
}
function closePopupSelections() {
    Selections.style.display = "none";
};

function checkScaleModes() {
    const width = window.innerWidth;
    const height = window.innerHeight;

    const width_windiw = Modes.offsetWidth;
    const height_windiw = Modes.offsetHeight;

    Modes.style.left = `${Math.floor(width/2)-Math.floor(width_windiw/2)}px`
    Modes.style.top = `${Math.floor(height/2)-Math.floor(height_windiw/2)}px`
}
function closePopupModes() {
    Modes.style.display = "none";
};

const additional_settings = document.getElementById("additional_settings");

if (document.getElementById("page_hidden").style.display === "none") {
    document.getElementById("page_hidden").style.display = ""
    document.getElementById("page_right").style.display = "none"

} else {
    document.getElementById("page_hidden").style.display = "none"
    document.getElementById("page_right").style.display = ""
};

const accept_additional_settings = document.getElementById("accept_additional_settings");
accept_additional_settings.addEventListener('click', () => {
    document.getElementById("page_hidden").style.display = "none"
    document.getElementById("page_right").style.display = ""
});


additional_settings.addEventListener('click', () => {
    if (document.getElementById("page_hidden").style.display === "none") {
        document.getElementById("page_hidden").style.display = ""
        document.getElementById("page_right").style.display = "none"
    } else {
        document.getElementById("page_hidden").style.display = "none"
        document.getElementById("page_right").style.display = ""
    };
});

closePopupModes();
closePopupRoles();
closePopupSelections();

document.getElementById("select_selections").addEventListener('click', () => {
//    console.log("Selections");
    Selections.style.display = "flex";
    checkScaleSelections()
    closePopupModes();
    closePopupRoles();
});
document.getElementById("select_mode").addEventListener('click', () => {
//    console.log("Modes");
    Modes.style.display = "flex";
    checkScaleModes()
    closePopupRoles();
    closePopupSelections();
});
document.getElementById("role_choose").addEventListener('click', () => {
//    console.log("Roles");
    Roles.style.display = "flex";
    checkScaleRoles()
    closePopupModes();
    closePopupSelections();
});
window.addEventListener('resize', checkScaleModes);
window.addEventListener('resize', checkScaleSelections);
window.addEventListener('resize', checkScaleRoles);

const select_button = document.querySelectorAll(".select_button");
select_button.forEach(item => {
    item.addEventListener('click', () => {
        if (item.dataset.type === "role") {
            document.getElementById("select_role_send").value = item.dataset.value
        } else if (item.dataset.type === "mode") {
            document.getElementById("select_game_mode_send").value = item.dataset.value
        };

        closePopupModes();
        closePopupRoles();
    });
});

const li_element = document.querySelectorAll(".li_element");
li_element.forEach(item => {
    item.addEventListener('click', () => {
        document.getElementById("select_selections_send").value = item.dataset.value
        closePopupSelections();
    });
});

//li_element_text.setAttribute('data-value', element.ID);
//const value = elem.dataset.value;