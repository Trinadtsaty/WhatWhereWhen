
const questions = document.querySelectorAll(".question_on_page");

const question_element_hidden = document.querySelectorAll(".question_element_hidden");
question_element_hidden.forEach(item => {
    item.style.display = "none";
});

questions.forEach(question => {
    question.addEventListener('click', () => {
        const status = question.dataset.status;
        if (status === "0") {
            question.dataset.status = "1";
            const question_elements_displayed = question.querySelectorAll(".question_element_displayed");
            question_elements_displayed.forEach(item => {
                item.style.display = "none";
            });
            const question_elements_hidden = question.querySelectorAll(".question_element_hidden");
            question_elements_hidden.forEach(item => {
                item.style.display = "";
            });
        } else {
            question.dataset.status = "0";
            const question_elements_displayed = question.querySelectorAll(".question_element_displayed");
            question_elements_displayed.forEach(item => {
                item.style.display = "";
            });
            const question_elements_hidden = question.querySelectorAll(".question_element_hidden");
            question_elements_hidden.forEach(item => {
                item.style.display = "none";
            });
        };
    });
});