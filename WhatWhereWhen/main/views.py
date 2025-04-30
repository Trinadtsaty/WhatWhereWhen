from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# def index(request):
#     return render(request, 'main/index.html')
# def questions(request):
#     return render(request, 'main/questions.html')

@login_required()
def Game_Room(request):
    return render(request, "main/main_game.html")