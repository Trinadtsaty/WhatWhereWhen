from idlelib.rpc import request_queue
from .models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

def question_main(request):
    # return render(request, "questions/question_main.html")
    title = 'Вопросы'
    return render(request, "questions/pattern.html", {"title" : title})


@login_required()
def question_add(request):
    return render(request, "questions/question_add.html")

@login_required()
def tag_add(request):
    ref = request.GET.get('ref')
    print(ref)
    return render(request, "questions/tag_add.html")


def question(request,question_number):
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
        estimation_ball=estimation_ball / estimations_len

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

