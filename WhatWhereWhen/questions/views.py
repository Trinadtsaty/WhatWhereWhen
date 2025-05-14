from idlelib.rpc import request_queue


from .models import *

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from registration.def_help import *
from registration.models import Users
from django.utils.html import escape
from .decorators import edit_question
from django.core.exceptions import ValidationError
from .models import Question
from django.http import JsonResponse


# def question_main(request):
#
#     title = 'Вопросы'
#     return render(request, "questions/question_main.html")



import json

def question_main(request):
    question_page=0
    count_question=5
    search = ""
    search_name = ""
    search_text = ""
    search_answer = ""
    search_tags_and = []
    search_tags_or = []
    author_question = []

    if request.method == 'POST':
        # Получение данных из POST-запроса
        data = json.loads(request.body)  # Читаем тело запроса
        test_data = data.get('test')  # Получаем значение 'test'
        print(data)
        # Обработка данных
        response_data = {'message': 'Данные получены', 'data': test_data}
        return JsonResponse(response_data)
        # return render(request, "questions/question_main.html", response_data)

    questions = Question.objects.filter(publication=True).order_by('ID')[0+(question_page*count_question):count_question+(question_page*count_question)]







    return render(request, "questions/question_main.html", {
        "questions":questions,
    })


@login_required()
def question_add(request):
    if request.method == 'POST':
        question_name = escape(request.POST.get('question_name').strip())
        text_question = escape(request.POST.get('text_question').strip())
        note = escape(request.POST.get('note').strip())
        answer = escape(request.POST.get('answer').strip())
        answer_description = escape(request.POST.get('answer_description').strip())

        if question_name:
            try:
                question_name_line(question_name)
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

        if text_question:
            try:
                question_name_text(text_question)
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


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
