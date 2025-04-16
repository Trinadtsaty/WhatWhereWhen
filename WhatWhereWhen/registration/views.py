from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Titles, Users_and_Titles, Users
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics
# from .serializers import Users_mainSerializer
from rest_framework.response import Response

def get_active_users():
    # Определяем временной порог для активности пользователей
    time_threshold = timezone.now() - timedelta(minutes=5)
    # Возвращаем количество пользователей, активных в последние 5 минут
    return Users.objects.filter(last_activity__gte=time_threshold).count()

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


def user_register(request):
    return render(request, "registration/registr.html")


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