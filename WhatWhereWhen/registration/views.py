from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Titles, Users_and_Titles, Users
from django.contrib.auth.decorators import login_required

from rest_framework import generics
from rest_framework.response import Response
from .def_help import *
import datetime


class Users_mainAPI(generics.ListAPIView):
    queryset = Users.objects.all()

    def list(self, request, *args, **kwargs):
        # Подсчитываем общее количество пользователей
        total_users = self.queryset.count()

        # Подсчитываем количество активных пользователей
        online_users = get_active_users()

        questions_count = "pass"
        room_online = "pass"

        # Формируем ответ с только необходимыми данными
        response_data = {
            'total_users': total_users,
            'online_users': online_users,
            'questions_count': questions_count,
            'room_online': room_online
        }

        return Response(response_data)

def user_login(request):
    if request.method == 'POST':
        usermail = request.POST.get('mail')
        password = request.POST.get('password')

        if usermail:
            try:
                validate_email_login(usermail)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "registration/login.html", {
                    'error': error,
                })
        if password:
            try:
                validate_password_login(password)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "registration/login.html", {
                    'usermail': usermail,
                    'error': error,
                })
        if not usermail or not password:
            return render(request, "registration/login.html", {
                'error': 'Пожалуйста заполните все поля',
                'usermail': usermail,
            })

        user = authenticate(request, email=usermail.lower(), password=password)
        if user is not None:
            login(request, user)
            return redirect('Menu')  # Перенаправление на домашнюю страницу после успешного входа
        else:
            return render(request, "registration/login.html", {
                'error': 'Неверная почта или пароль',
                'usermail': usermail,  # Сохраняем введенное имя пользователя
            })  # Передаем ошибку обратно на страницу
    return render(request, "registration/login.html")

def menu(request):
    # Извлечение всех титулов
    titles = Titles.objects.all()
    # Извлечение всех связей пользователей и титулов
    users_and_titles = Users_and_Titles.objects.select_related('users', 'titles_units').all()

    # Передача данных в контекст
    context = {
        'titles': titles,
        'users_and_titles': users_and_titles,
        'user_active': get_active_users(),
        'user_count': Users.objects.count(),
    }


    return render(request, "registration/main_page.html", context)

def custom_logout(request):
    next_url = request.META.get('HTTP_REFERER', '/')
    logout(request)
    return redirect(next_url)

def user_register(request):
    if request.method == 'POST':
        mail = request.POST.get('e-mail')
        username = request.POST.get('nick_name')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        image = request.FILES.get('image_user')

        if username:
            try:
                validate_name(username)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "registration/registr.html", {
                    'error': error,
                })

        if mail:
            try:
                validate_email(mail)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "registration/registr.html", {
                    'username': username,
                    'error': error,
                })

        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "registration/registr.html", {
                    'username': username,
                    'email': mail,
                    'error': error,
                })

        if password != password_repeat:
            return render(request, "registration/registr.html", {
                'error': 'Пароли не совпадают',
                'username': username,
                'email': mail,
            })

        if not username or not password or not password_repeat or not mail:
            return render(request, "registration/registr.html", {
                'error': 'Пожалуйста заполните все поля',
                'username': username,
                'email': mail,
            })

        if image:
            try:
                validate_image(image)
            except ValidationError as e:
                error = str(e) [2:-2]
                return render(request, "registration/registr.html", {
                    'error': error,
                    'username': username,
                    'email': mail,
                })

        user = Users.objects.create_user(
            login=username,
            email=mail.lower(),
            password=password,
            picture=image
        )

        titles_start, created = Titles.objects.get_or_create(titles_name=f"Добо пожаловать {datetime.datetime.now().year}")
        if created:
            titles_start.titles_name = f"Добо пожаловать {datetime.datetime.now().year}"
            titles_start.titles_description = f"Вы участник {datetime.datetime.now().year-2025}-го сезона тестирования сайта, спасибо вам"
            titles_start.save()

        titles_give, created_give = Users_and_Titles.objects.get_or_create(users=user, titles_units=titles_start)
        if created_give:
            titles_give.save()

        login(request, user)
        if image:
            Users_bd, created = Users.objects.get_or_create(email=request.user.email)
            new_file_name = f"IMG/Users/{request.user.ID}_{datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.{image.name.split('.')[-1]}"
            path = default_storage.save(new_file_name, image)
            Users_bd.login = username
            Users_bd.picture = path
            Users_bd.save()

        return redirect('Menu')
    return render(request, "registration/registr.html")


@login_required()
def change_profile(request):
    if request.method == 'POST':
        username = request.POST.get('nick_name')
        image = request.FILES.get('image_user')

        if username:
            try:
                validate_name(username)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "registration/change.html", {
                    'error': error,
                })

        if image:
            try:
                validate_image(image)
            except ValidationError as e:
                error = str(e) [2:-2]
                return render(request, "registration/change.html", {
                    'error': error,
                    'username': username,
                })

        Users_bd, created = Users.objects.get_or_create(email=request.user.email)
        if not created:
            if image:
                new_file_name = f"IMG/Users/{request.user.ID}_{datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.{image.name.split('.')[-1]}"  # Используем расширение оригинального файла

                # Сохраняем файл с новым именем
                path = default_storage.save(new_file_name, image)  # Используем image напрямую

                # Обновляем поле picture новым путем
                Users_bd.login = username
                Users_bd.picture = path  # Сохраняем путь к новому файлу
                Users_bd.save()
            else:
                Users_bd.login = username
                Users_bd.save()

            return redirect('Menu')
    return render(request, "registration/change.html")



def hint(request):
    return render(request, "registration/plug.html")

def author(request):
    return render(request, "registration/plug.html")
