from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.html import escape

# def index(request):
#     return render(request, 'main/index.html')
# def questions(request):
#     return render(request, 'main/questions.html')


def Game_Room(request):
    return render(request, "main/main_game.html")

@login_required()
def Create_Room(request):
    if request.method == 'POST':
        name = escape(request.POST.get('room_name'))
        close = escape(request.POST.get('room_close'))
        password = escape(request.POST.get('room_password'))
        selection = escape(request.POST.get('select_selections_send'))
        mode = escape(request.POST.get('select_game_mode_send'))
        role = escape(request.POST.get('select_role_send'))
        people_limit = escape(request.POST.get('room_people_limit'))
        early_answer = escape(request.POST.get('room_early_answer'))
        time_early_answer = escape(request.POST.get('room_time_early_answer'))
        chat_clean = escape(request.POST.get('room_chat_clean'))
        time_question = escape(request.POST.get('room_time_question'))
        show_question = escape(request.POST.get('room_show_question'))
        reading_speed = escape(request.POST.get('room_reading_speed'))
        random_order = escape(request.POST.get('room_random_order'))
        break_questions = escape(request.POST.get('room_break_questions'))

        output = {
            "name":name,
            "close": close,
            "password": password,
            "selection": selection,
            "mode": mode,
            "role": role,
            "people_limit": people_limit,
            "early_answer": early_answer,
            "time_early_answer": time_early_answer,
            "chat_clean": chat_clean,
            "time_question": time_question,
            "show_question": show_question,
            "reading_speed": reading_speed,
            "random_order": random_order,
            "break_questions": break_questions,
        }

        # print(output)



    return render(request, "main/create_room.html")