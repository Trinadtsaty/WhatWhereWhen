from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        usermail = request.POST.get('mail')
        password = request.POST.get('password')
        user = authenticate(request, email=usermail, password=password)
        if user is not None:
            login(request, user)
            return redirect('Menu')  # Перенаправление на домашнюю страницу после успешного входа
        else:
            return render(request, "registration/login.html", {
                'error': 'Неверная почта или пароль',
                'username': usermail,  # Сохраняем введенное имя пользователя
            })  # Передаем ошибку обратно на страницу
    return render(request, "registration/login.html")


def user_register(request):
    return render(request, "registration/registr.html")

def menu(request):
    return render(request, "registration/main_page.html")