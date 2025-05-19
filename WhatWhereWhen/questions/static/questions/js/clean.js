const clean= document.querySelector('#clean_button');

clean.addEventListener('click', ()=> {
    document.getElementById('question_search_title').value = "";
    document.getElementById('question_search_text').value = "";
    document.getElementById('question_search_answer').value = "";
    document.getElementById('checkbox_search').checked = false;
    document.getElementById('checkbox_tag').checked = false;
    document.getElementById('question_search').value = "";

    select_author.length = 0;
    unselect_author.length = 0;
    select_tag.length = 0;
    unselect_tag.length = 0;

    document.querySelectorAll('.select_item').forEach(item => {
        item.querySelector('.check_mark_box').querySelector('.select').style.display = 'none';
        item.querySelector('.check_mark_box').querySelector('.unselect').style.display = 'none';
        item.querySelector('.check_mark_box').querySelector('.base').style.display = '';
    });

    Timer()
});