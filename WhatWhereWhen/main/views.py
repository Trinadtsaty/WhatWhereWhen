from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')
def questions(request):
    return render(request, 'main/questions.html')