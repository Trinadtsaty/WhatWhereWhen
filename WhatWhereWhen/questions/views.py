from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from registration.def_help import *

from registration.models import Users
from django.utils.html import escape
from .decorators import edit_question
from django.core.exceptions import ValidationError
from .models import Question
from django.http import JsonResponse
import json
from django.db.models import Q, Count, Avg, Value
from django.db.models.functions import Coalesce, Round

def question_note(name):
    if len(name) > 700:
        raise ValidationError('Текст описания вопроса слишком длинный, пожалуйста придумайте описание о 700 символов')

def question_answer_name(name):
    if len(name) < 3:
        raise ValidationError('Текст ответа слишком короткий, пожалуйста придумайте ответ от 3 до 50 символов')
    if len(name) > 50:
        raise ValidationError('Текст ответа слишком длинный, пожалуйста придумайте ответ от 3 до 50 символов')

def question_name_text_edit(name):
    if len(name) < 20:
        # print(name)
        raise ValidationError('Текст вопроса слишком короткий, пожалуйста придумайте вопрос от 20 до 1000 символов')
    if len(name) > 1000:
        raise ValidationError('Текст вопроса слишком длинный, пожалуйста придумайте вопрос от 20 до 1000 символов')


def question_name_line(name):
    if Question.objects.filter(question_name=name).exists():
        raise ValidationError('Вопрос с таким названием уже существует')

    if not (5 <= len(name) <= 50):
        raise ValidationError('Название вопроса должно быть длиной от 5 до 50 символов')


from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Lower

@csrf_exempt
def question_main(request):
    if request.method == 'POST':
        # Получение данных из POST-запроса
        data = json.loads(request.body)  # Читаем тело запроса

        data_get = chek_json_filter(data)

        # Получаем вопросы, которые опубликованы
        questions = Question.objects.filter(publication=True)

        # Фильтрация по поисковым запросам
        if data_get.get("search"):
            questions = questions.filter(
                Q(question_name__icontains=data_get["search"]) |
                Q(text_question__icontains=data_get["search"]) |
                Q(answer__icontains=data_get["search"])
            )
        elif data_get.get("search_name") or data_get.get("search_text") or data_get.get("search_answer"):
            query = Q()
            if data_get.get("checkbox_search"):
                if data_get.get("search_name"):
                    query &= Q(question_name__icontains=data_get["search_name"])

                if data_get.get("search_text"):
                    query &= Q(text_question__icontains=data_get["search_text"])

                if data_get.get("search_answer"):
                    query &= Q(answer__icontains=data_get["search_answer"])

                questions = questions.filter(query)

            else:
                if data_get.get("search_name"):
                    query |= Q(question_name__icontains=data_get["search_name"])

                if data_get.get("search_text"):
                    query |= Q(text_question__icontains=data_get["search_text"])

                if data_get.get("search_answer"):
                    query |= Q(answer__icontains=data_get["search_answer"])

                questions = questions.filter(query)

        # filename="logs.txt"
        # with open(filename, 'w', encoding='utf-8') as file:
        #     file.write("Фильтрация по поисковым запросам" + str(questions) + '\n')

        # Фильтрация по тегам
        if data_get.get("select_tag"):
            query = Q()

            # with open(filename, 'a', encoding='utf-8') as file:
            #     file.write("Список допущенных тегов" + str(data_get["select_tag"]) + '\n')

            for id in data_get["select_tag"]:
                query |= Q(Question_Tag__tags_id=id)
            questions = questions.filter(query)
            questions_solo = questions.filter(query).distinct()

            if data_get.get("coincidence_tag"):
                query = Q()
                for question in questions_solo:
                    count = questions.filter(ID=question.ID).count()
                    # with open(filename, 'a', encoding='utf-8') as file:
                    #     file.write(f"Элемент {question} повторяется {count} раз\n")
                    if count == len(data_get["select_tag"]):
                        query |= Q(ID=question.ID)
                questions = questions_solo.filter(query)

        # with open(filename, 'a', encoding='utf-8') as file:
        #     file.write("Фильтрация по тегам" + str(questions) + '\n')

        # Исключение тегов
        if data_get.get("unselect_tag"):
            exclude = Q()
            for item in data_get["unselect_tag"]:
                exclude |= Q(Question_Tag__tags_id=item)
            questions = questions.exclude(exclude)

        # with open(filename, 'a', encoding='utf-8') as file:
        #     file.write("Исключение тегов" + str(questions) + '\n')

        # Фильтрация по авторам
        if data_get.get("select_author"):
            query = Q()
            for item in data_get["select_author"]:
                query |= Q(question_author=item)

            questions = questions.filter(query)

        # with open(filename, 'a', encoding='utf-8') as file:
        #     file.write("Фильтрация по авторам" + str(questions) + '\n')

        # Исключение по авторам
        if data_get.get("unselect_author"):
            exclude = Q()
            for item in data_get["unselect_author"]:
                exclude |= Q(question_author=item)  # Исправлено на правильное поле

            questions = questions.exclude(exclude)

        # with open(filename, 'a', encoding='utf-8') as file:
        #     file.write("Исключение по авторам" + str(questions) + '\n')

        #Считаем среднюю оценку
        questions=questions.annotate(average_estimation=Coalesce(Round(Avg('Question__estimation'), 1), Value(0.0)))

        # with open(filename, 'a', encoding='utf-8') as file:
        #     file.write("Считаем среднюю оценку" + str(questions) + '\n')

        questions=questions.order_by(data_get.get("sorting_question"))[0+(data_get.get("count_question")*data_get.get("question_page")):data_get.get("count_question")+(data_get.get("count_question")*data_get.get("question_page"))]

        # with open(filename, 'a', encoding='utf-8') as file:
        #     file.write("Отбираем нужное кол-во фильтруем порядок" + str(questions) + '\n')

        questions_data = list(questions.values('ID', 'question_name','average_estimation', 'text_question'))  # Укажите поля, которые хотите вернуть

        # with open(filename, 'a', encoding='utf-8') as file:
        #     file.write("Передаваемый массив списков" + str(questions_data))

        response_data = {'message': 'Данные получены', 'questions': questions_data}

        return JsonResponse(response_data)

    authors =  Question.objects.filter(publication=True).values_list('question_author', flat=True)
    authors = list(set(authors))
    users = Users.objects.filter(ID__in=authors)
    tags = Tags.objects.filter(publication=True)

    if request.user.is_authenticated:
        selection_user = Selections.objects.filter(publication=True, selection_author=request.user)

        return render(request, "questions/question_main.html", {
            "tags":tags,
            "authors":users,
            "selection_user":selection_user

        })

    return render(request, "questions/question_main.html", {
        "tags":tags,
        "authors":users,
    })


@login_required()
def question_add(request):
    if request.method == 'POST':
        question_name = escape(request.POST.get('question_name').strip())
        text_question = escape(request.POST.get('text_question').strip())
        note = escape(request.POST.get('note').strip())
        answer = escape(request.POST.get('answer').strip())
        answer_description = escape(request.POST.get('answer_description').strip())

        if not question_name or not text_question or not answer:
            return render(request, "registration/registr.html", {
                'error': 'Я рад, что вы демонстрируете ваши навыки програмирования, однако пожалуйста заполните поля в ручную',
                'question_name': question_name,
                'text_question': text_question,
                'answer': answer,
            })

        if question_name:

            try:
                question_name_line(question_name)
            except ValidationError as e:
                error = str(e).strip("string=")

                print(error
                      )
                return render(request, "questions/question_add.html", {
                    'error': error,
                    'submit': "Отправить",
                    "question_name": question_name,
                    "text_question": text_question,
                    "note": note,
                    "answer": answer,
                    "answer_description": answer_description
                })

        if text_question:
            try:
                question_name_text(text_question)
            except ValidationError as e:
                print(e.string)
                error = str(e)[2:-2]
                return render(request, "questions/question_add.html", {
                    'error': error,
                    'submit': "Отправить",
                    "question_name": question_name,
                    "text_question": text_question,
                    "note": note,
                    "answer": answer,
                    "answer_description": answer_description
                })

        if answer:
            try:
                question_answer_name(answer)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "questions/question_add.html", {
                    'error': error,
                    'submit': "Отправить",
                    "question_name": question_name,
                    "text_question": text_question,
                    "note": note,
                    "answer": answer,
                    "answer_description": answer_description
                })

        if note:
            try:
                question_note(note)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "questions/question_add.html", {
                    'error': error,
                    'submit': "Отправить",
                    "question_name": question_name,
                    "text_question": text_question,
                    "note": note,
                    "answer": answer,
                    "answer_description": answer_description
                })

        if answer_description:
            try:
                question_answer_text(answer_description)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "questions/question_add.html", {
                    'error': error,
                    'submit': "Отправить",
                    "question_name": question_name,
                    "text_question": text_question,
                    "note": note,
                    "answer": answer,
                    "answer_description": answer_description
                })

        question = Question(question_name=question_name, text_question=text_question, note=note, answer=answer, answer_description=answer_description, license_id=Licenses.objects.get(ID=1), question_author=request.user)
        question.save()
        return redirect('Question', question_number=question.ID)


    return render(request, "questions/question_add.html", {'submit': "Отправить",})




@edit_question
def question_edit(request, question_number):
    # Получаем объект question по его ID
    question = get_object_or_404(Question, ID=question_number)


    # Инициализация полей
    question_name = question.question_name
    text_question = question.text_question
    note = question.note
    answer = question.answer
    answer_description = question.answer_description

    if request.method == 'POST':
        question_name = escape(request.POST.get('question_name', '').strip())
        text_question = escape(request.POST.get('text_question', '').strip())
        note = escape(request.POST.get('note', '').strip())
        answer = escape(request.POST.get('answer', '').strip())
        answer_description = escape(request.POST.get('answer_description', '').strip())

        errors = []  # Список для хранения ошибок

        # Проверка и валидация каждого поля
        if question_name:
            try:
                question_name_line_edit(question_name)
            except ValidationError as e:
                errors.append(str(e)[2:-2])

        if text_question:
            try:
                question_name_text_edit(text_question)
            except ValidationError as e:
                errors.append(str(e)[2:-2])

        if answer:
            try:
                question_answer_name(answer)
            except ValidationError as e:
                errors.append(str(e)[2:-2])

        if note:
            try:
                question_note(note)
            except ValidationError as e:
                errors.append(str(e)[2:-2])

        if answer_description:
            try:
                question_answer_text(answer_description)
            except ValidationError as e:
                errors.append(str(e)[2:-2])

        if errors:
            return render(request, "questions/question_add.html", {
                'error': errors[0],
                'submit': "Сохранить",
                "question_name": question_name,
                "text_question": text_question,
                "note": note,
                "answer": answer,
                "answer_description": answer_description
            })

        # Сохраняем изменения в объекте question
        question.question_name = question_name
        question.text_question = text_question
        question.note = note
        question.answer = answer
        question.answer_description = answer_description

        question.save()

        # Перенаправление на страницу вопроса
        return redirect('Question', question_number=question.ID)  # Используем ID вопроса

    # Если метод GET, отображаем форму с текущими данными
    return render(request, "questions/question_add.html", {
        'submit': "Сохранить",
        "question_name": question_name,
        "text_question": text_question,
        "note": note,
        "answer": answer,
        "answer_description": answer_description
    })



@login_required()
def tag_add(request):
    ref = request.GET.get('ref')
    try:
        ref=int(ref)
    except:
        pass
    if request.method == 'POST':
        tag = request.POST.get('tag_name')

        if tag:
            try:
                validate_tag(tag)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "questions/tag_add.html", {
                    'error': error,
                })

            exists = Tags.objects.filter(tag_name=tag)

            if exists:
                error = "Такой тег уже существует"
                return render(request, "questions/tag_add.html", {
                    'error': error,
                })
            else:
                Tags_bd, created = Tags.objects.get_or_create(tag_name=tag, tag_author=request.user)
                Tags_bd.save()


                if isinstance(ref, int):
                    return redirect('Question', question_number=ref)
                else:
                    return redirect('Question_add')

    return render(request, "questions/tag_add.html")


def question(request, question_number):
    question = get_object_or_404(Question, ID=question_number, publication=True)
    tags_queation=[]
    tags_questions = Tags_Questions.objects.filter(question_id = question)
    for tag in tags_questions:
        if tag.tags_id.publication:
            tags_queation.append(tag.tags_id.tag_name)

    estimations = Estimation_Quest_User.objects.filter(question = question)
    tags = Tags.objects.filter(publication = True)
    tags_all=[]
    for tag in tags:
        if tag.tag_name not in tags_queation:
            tags_all.append(tag)

    estimation_ball=0
    my_estimation = None
    estimation_ball_bol = False
    estimations_len=estimations.count()
    if estimations_len>0:
        for est in estimations:
            estimation_ball+=est.estimation
            if est.user == request.user:
                my_estimation = est.estimation
                estimation_ball_bol = True
        estimation_ball = round(estimation_ball / estimations_len, 1)

    return render(request, "questions/question.html", {
        "number" : question_number,
        "title" : 'Страница вопроса',
        "tags_all":tags_all,
        "tags_queation" : tags_queation,
        "Question":question,
        "estimation_ball": estimation_ball,
        "estimation_ball_bol": estimation_ball_bol,
        "my_estimation": my_estimation,
    })


from .class_help import *
from rest_framework.permissions import IsAuthenticated

class Question_Evaluation_API(Question_Evaluation_APIUpdate, Question_Evaluation_APICreate):
    permission_classes = (IsAuthenticated, )
    # pass

class Tag_Question_API(Tag_Question_APICreate):
    permission_classes = (IsAuthenticated, )
    # pass

class Selection_Questions_API(Selection_Questions_APICreate, Selection_Questions_APIDestroy):
    permission_classes = (IsAuthenticated,)

class Selection_API(SelectionsByQuestionAPIView):
    permission_classes = (IsAuthenticated,)



@login_required()
def selectionCreate(request):
    if request.method == 'POST':
        selection_name = escape(request.POST.get('selection_name', '').strip())
        selection_checkbox = request.POST.get('selection_checkbox')

        if selection_checkbox:
            selection_checkbox_bd=True
        else:
            selection_checkbox_bd=False

        if selection_name:
            try:
                validate_selection(selection_name)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "questions/selection_create.html", {
                    'error': error,
                    "selection_name":selection_name,
                    "selection_checkbox": selection_checkbox_bd,
                })

        selections, created = Selections.objects.get_or_create(selection_name=selection_name, private=selection_checkbox_bd, selection_author=request.user)
        if created:
            selections.save()

    return render(request, "questions/selection_create.html")

@login_required()
def questionClaim(request, question_number):
    question = get_object_or_404(Question, ID=question_number, publication=True)
    if request.method == 'POST':
        claim_name = escape(request.POST.get('claim_name', '').strip())
        text_claim = escape(request.POST.get('text_claim', '').strip())

        if not claim_name and not text_claim:
            return render(request, "questions/claim_question.html", {
                'error': 'Пожалуйста заполните все поля',
                "question_name":question.question_name,
                "claim_name":claim_name,
                "text_claim":text_claim,
            })

        if text_claim:
            try:
                Claim_text(text_claim)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "questions/claim_question.html", {
                    'error': error,
                    "claim_name":claim_name,
                    "text_claim":text_claim,
                })

        complaints, created = Complaints_Questions.objects.get_or_create(question_id=question, complaint_name=claim_name, complaint_description=text_claim, complaint_author=request.user)
        if created:
            complaints.save()

    return render(request, "questions/claim_question.html", {
        "question_name":question.question_name,
    })

def selectionClaim(request):
    return render(request, "questions/plug.html")


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
