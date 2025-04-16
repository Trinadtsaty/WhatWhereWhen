from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Titles, Users_and_Titles, Users

from rest_framework import generics
# from .serializers import Users_mainSerializer
from rest_framework.response import Response
from .def_help import *


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


# class Users_mainAPI(generics.ListAPIView):
#     queryset = Users.objects.all()
#     serializer_class = Users_mainSerializer
#
#     def list(self, request, *args, **kwargs):
#         # Получаем список пользователей и сериализуем его
#         users = self.get_queryset()
#         serializer = self.get_serializer(users, many=True)
#
#         # Подсчитываем общее количество пользователей
#         total_users = self.queryset.count()
#
#         # Подсчитываем количество активных пользователей
#         online_users = get_active_users()
#
#         # Формируем ответ
#         response_data = {
#             'users': serializer.data,
#             'total_users': total_users,
#             'online_users': online_users
#         }
#
#         return Response(response_data)

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

        if mail:
            try:
                validate_email(mail)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "registration/registr.html", {
                    'error': error,
                })

        if username:
            try:
                validate_name(username)
            except ValidationError as e:
                error = str(e)[2:-2]
                return render(request, "registration/registr.html", {
                    'email': mail,
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
            email=mail,
            password=password,
            picture=image
        )
        login(request, user)
        return redirect('Menu')
    return render(request, "registration/registr.html")

