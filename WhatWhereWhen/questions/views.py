from django.shortcuts import render

# Create your views here.

def Question_main(request):
    return render(request, "questions/question_main.html")