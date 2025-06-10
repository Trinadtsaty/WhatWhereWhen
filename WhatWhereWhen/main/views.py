from dbm import error
from idlelib.rpc import request_queue
from django.db.models import Q
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.core.exceptions import ValidationError
from .models import *
from questions.models import *
from django.urls import reverse


# def index(request):
#     return render(request, 'main/index.html')
# def questions(request):
#     return render(request, 'main/questions.html')

def True_False(element):
    if element == "on":
        return True
    else:
        return False

def Game_Room(request):
    error = request.GET.get('err')
    rooms = game_rooms.objects.all()
    if error:
        return render(request, "main/main_game.html", {
            "rooms": rooms,
            "error": error,
        })
    return render(request, "main/main_game.html",{"rooms":rooms})


@login_required()
def Create_Room(request):
    user_creator = request.user
    query = Q(publication=True)
    additional_conditions = Q()
    additional_conditions |= Q(private=False) & ~Q(selection_author=user_creator)
    additional_conditions |= Q(selection_author=user_creator)
    query &= additional_conditions
    Selection_on_page = Selections.objects.filter(query)

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
        description = escape(request.POST.get('room_description'))

        output = {
            "name": name,
            "close": True_False(close),
            "password": password,
            "selection": selection,
            "mode": mode,
            "role": role,
            "people_limit": people_limit,
            "early_answer": True_False(early_answer),
            "time_early_answer": time_early_answer,
            "chat_clean": True_False(chat_clean),
            "time_question": time_question,
            "show_question": True_False(show_question),
            "reading_speed": reading_speed,
            "random_order": True_False(random_order),
            "break_questions": break_questions,
            "description" : description,
        }
        output["Selections_on_page"] = Selection_on_page

        try:
            if name:
                if len(name) < 3 or len(name) > 20:
                    raise ValidationError('Пожалуйста введите имя комнаты длинной от 3 до 20 символов')
                if game_rooms.objects.filter(room_name=name).exists():
                    raise ValidationError('Комната с таким названием уже существует, пожалуйста смените имя')
            else:
                raise ValidationError('Заполните поле "Название сессии"')
            if output["close"]:
                if password:
                    if len(password) > 20:
                        raise ValidationError('Пожалуйста придумайте пароль длинной до 20 символов')
                else:
                    raise ValidationError('Пожалуйста введите пароль или сделайте сессию открытой')
            if output["selection"]:
                if not Selections.objects.filter(ID=output["selection"]).exists():
                    raise ValidationError('Ваша коллекция не существует, пожалуйста укажите верное значение')
                selection = Selections.objects.get(ID=output["selection"])
                if selection.private and selection.selection_author != user_creator:
                    raise ValidationError('Данная коллекция является закрытой!!!')
                if not selection.publication:
                    raise ValidationError('Данная коллекция была удалена')
            else:
                raise ValidationError('Выберите коллекцию вопросов')
            if output["mode"]:
                if not (output["mode"] == 'classic' or output["mode"] == 'sport' or output["mode"] == 'collective_answer'):
                    raise ValidationError('Указан неверный игровой режим')
            else:
                raise ValidationError('Выберите режим игры')
            if output["role"]:
                if not (output["role"] == 'leader' or output["role"] == 'captain' or output["role"] == 'player'):
                    raise ValidationError('Указан неверная роль хоста')
            else:
                raise ValidationError('Выберите роль хоста')
            if output["people_limit"]:
                try:
                    int(output["people_limit"])
                except:
                    raise ValidationError('Укажите числом кол-во игроков')
                if int(output["people_limit"]) < 3 or int(output["people_limit"]) > 8:
                    raise ValidationError('Укажите число игроков от 3 до 8 человек')
            else:
                raise ValidationError('Укажите кол-во игроков')
            if output["early_answer"]:
                if output["time_early_answer"]:
                    try:
                        int(output["time_early_answer"])
                    except:
                        raise ValidationError('Время досрочного ответа должно быть числом')
                    if int(output["time_early_answer"]) < 5 or int(output["time_early_answer"]) > 600:
                        raise ValidationError('Время досрочного ответа должно быть от 5 до 600 секунд')
                else:
                    raise ValidationError('Укажите время на досрочный ответ')
            if output["time_question"]:
                try:
                    int(output["time_question"])
                except:
                    raise ValidationError('Время на вопрос должно быть числом')
                if int(output["time_question"]) < 10 or int(output["time_question"]) > 600:
                    raise ValidationError('Время на вопрос должно быть от 10 до 600 секунд')
            else:
                raise ValidationError('Укажите время на вопрос')
            if output["reading_speed"]:
                try:
                    int(output["reading_speed"])
                except:
                    raise ValidationError('Скорость чтения должна быть числом')
                if int(output["reading_speed"]) < 1 or int(output["reading_speed"]) > 60:
                    raise ValidationError('Скорость чтения должна быть от 1 до 60 символов в секунду')
            else:
                raise ValidationError('УКажите скорость чтения')
            if output["break_questions"]:
                try:
                    int(output["break_questions"])
                except:
                    raise ValidationError('Перерыв между вопросами должен быть числом')
                if int(output["break_questions"]) < 0 or int(output["break_questions"]) > 600:
                    raise ValidationError('Перерыв между вопросами должен быть от 0 до 600 секунд')
            else:
                raise ValidationError('Укажите время перерыва между вопросами')
            if output["description"]:
                if len(output["description"]) > 500:
                    output["description"] = output["description"][:497]+'...'
                    raise ValidationError('Описание комнаты должно быть до 500 символов')
        except ValidationError as e:
            output["error"] = str(e)[2:-2]
            return render(request, "main/create_room.html", output)

        if output["mode"] == 'classic':
            game_mode = 0
        elif output["mode"] == 'sport':
            game_mode = 1
        else:
            game_mode = 2

        if output["role"] == 'leader':
            Room, created = game_rooms.objects.get_or_create(
                room_name=output["name"],
                clos_room=output["close"],
                password_room=output["password"],
                selections=Selections.objects.get(ID=output["selection"]),
                game_mode=game_mode,
                host=user_creator,
                leader=user_creator,
                room_limit=output["people_limit"],
                people_on_page={"users":[user_creator.ID]},
                room_description=output["description"],
                early_answer=output["early_answer"],
                time_answer=output["time_early_answer"],
                clear_chat=output["chat_clean"],
                question_time=output["time_question"],
                show_question=output["show_question"],
                reading_speed=output["reading_speed"],
                random_order=output["random_order"],
                break_between_questions=output["break_questions"],
            )
        elif output["role"] == 'captain':
            Room, created = game_rooms.objects.get_or_create(
                room_name=output["name"],
                clos_room=output["close"],
                password_room=output["password"],
                selections=Selections.objects.get(ID=output["selection"]),
                game_mode=game_mode,
                host=user_creator,
                captain=user_creator,
                room_limit=output["people_limit"],
                people_on_page={"users":[user_creator.ID]},
                room_description=output["description"],
                early_answer=output["early_answer"],
                time_answer=output["time_early_answer"],
                clear_chat=output["chat_clean"],
                question_time=output["time_question"],
                show_question=output["show_question"],
                reading_speed=output["reading_speed"],
                random_order=output["random_order"],
                break_between_questions=output["break_questions"],
            )
        else:
            Room, created = game_rooms.objects.get_or_create(
                room_name=output["name"],
                clos_room=output["close"],
                password_room=output["password"],
                selections=Selections.objects.get(ID=output["selection"]),
                game_mode=game_mode,
                host=user_creator,
                room_limit=output["people_limit"],
                people_on_page={"users":[user_creator.ID]},
                room_description=output["description"],
                early_answer=output["early_answer"],
                time_answer=output["time_early_answer"],
                clear_chat=output["chat_clean"],
                question_time=output["time_question"],
                show_question=output["show_question"],
                reading_speed=output["reading_speed"],
                random_order=output["random_order"],
                break_between_questions=output["break_questions"],
            )

        if created:
            Room.save()
            request.session[f'access_{Room.ID}'] = True
            return redirect('Room', room_number=Room.ID)

        else:
            output["error"] = "Комната уже существует"
            return render(request, "main/create_room.html", output)


    return render(request, "main/create_room.html", {
        "close": False,
        "early_answer": True,
        "chat_clean": True,
        "show_question": True,
        "random_order": True,
        'Selections_on_page':Selection_on_page,
    })


@login_required()
def Room(request, room_number):
    room = get_object_or_404(game_rooms, ID=room_number)
    if room.clos_room:
        if not request.session.get(f'access_{room_number}'):
            return redirect(reverse('Room_passwoed') + f'?pas={room_number}')
    user_on_page = request.user

    array = room.people_on_page['users']

    if len(array) < room.room_limit and user_on_page.ID not in array:
        room.people_on_page['users'].append(user_on_page.ID)
        room.save()
    elif len(array) <= room.room_limit and user_on_page.ID in array:
        pass
    else:
        return redirect(reverse('Game_Room') + f'?err=Комната заполнена')
    # Получаем последние 50 сообщений из БД
    messages = ChatMessage.objects.filter(room=game_rooms.objects.get(ID=room_number)).order_by('-timestamp')[:50]


    selection = room.selections
    questions = Question.objects.filter(Question_Select__selection_id=selection)

    # print(questions)

    if request.method == 'POST':
        early_answer = escape(request.POST.get('room_early_answer'))
        time_early_answer = escape(request.POST.get('room_time_early_answer'))
        chat_clean = escape(request.POST.get('room_chat_clean'))
        time_question = escape(request.POST.get('room_time_question'))
        show_question = escape(request.POST.get('room_show_question'))
        reading_speed = escape(request.POST.get('room_reading_speed'))
        random_order = escape(request.POST.get('room_random_order'))
        break_questions = escape(request.POST.get('room_break_questions'))



        output = {
            "early_answer":True_False(early_answer),
            "time_early_answer":time_early_answer,
            "chat_clean":True_False(chat_clean),
            "time_question":time_question,
            "show_question":True_False(show_question),
            "reading_speed":reading_speed,
            "random_order":True_False(random_order),
            "break_questions":break_questions,

            "user": user_on_page,
            "room" : room,
            'messages': messages,
            'questions':questions,
        }

        try:

            if output["early_answer"]:
                if output["time_early_answer"]:
                    try:
                        int(output["time_early_answer"])
                    except:
                        raise ValidationError('Время досрочного ответа должно быть числом')
                    if int(output["time_early_answer"]) < 5 or int(output["time_early_answer"]) > 600:
                        raise ValidationError('Время досрочного ответа должно быть от 5 до 600 секунд')
                else:
                    raise ValidationError('Укажите время на досрочный ответ')

            if output["time_question"]:
                try:
                    int(output["time_question"])
                except:
                    raise ValidationError('Время на вопрос должно быть числом')
                if int(output["time_question"]) < 10 or int(output["time_question"]) > 600:
                    raise ValidationError('Время на вопрос должно быть от 10 до 600 секунд')
            else:
                raise ValidationError('Укажите время на вопрос')

            if output["reading_speed"]:
                try:
                    int(output["reading_speed"])
                except:
                    raise ValidationError('Скорость чтения должна быть числом')
                if int(output["reading_speed"]) < 1 or int(output["reading_speed"]) > 60:
                    raise ValidationError('Скорость чтения должна быть от 1 до 60 символов в секунду')
            else:
                raise ValidationError('УКажите скорость чтения')

            if output["break_questions"]:
                try:
                    int(output["break_questions"])
                except:
                    raise ValidationError('Перерыв между вопросами должен быть числом')
                if int(output["break_questions"]) < 0 or int(output["break_questions"]) > 600:
                    raise ValidationError('Перерыв между вопросами должен быть от 0 до 600 секунд')
            else:
                raise ValidationError('Укажите время перерыва между вопросами')

        except ValidationError as e:
            output["error"] = str(e)[2:-2]
            return render(request, "main/room.html", output)

        room = game_rooms.objects.get(ID=room_number)
        room.early_answer = output["early_answer"]
        room.time_answer = output["time_early_answer"]
        room.clear_chat = output["chat_clean"]
        room.question_time = output["time_question"]
        room.show_question = output["show_question"]
        room.reading_speed = output["reading_speed"]
        room.random_order = output["random_order"]
        room.break_between_questions = output["break_questions"]
        room.save()

        return render(request, "main/room.html", output)

    return render(request, "main/room.html", {
        "user": user_on_page,
        "room" : room,
        'messages': messages,
        'questions':questions,
        "early_answer": True,
        "chat_clean": True,
        "show_question": True,
        "random_order": True,
    })


@login_required()
def Password_Room(request):
    ref_value = request.GET.get('pas')
    room = get_object_or_404(game_rooms, ID=ref_value)
    if request.method == 'POST':
        password = escape(request.POST.get('room_password'))
        if room.password_room == password:
            request.session[f'access_{ref_value}'] = True
            return redirect('Room', room_number=ref_value)
        else:
            return render(request, "main/password_room.html", {
                "error": "Неверный пароль",
            })
    return render(request, "main/password_room.html")

@login_required()
def logout_secret(request, room_number):
    room = get_object_or_404(game_rooms, ID=room_number)
    if room.clos_room:
        if f'access_{room_number}' in request.session:
            del request.session[f'access_{room_number}']
    # room.people_on_page["users"].remove(request.user.ID)
    # room.save()
    # return redirect(reverse('Room_passwoed') + f'?pas={room_number}')
    return redirect('Game_Room')

