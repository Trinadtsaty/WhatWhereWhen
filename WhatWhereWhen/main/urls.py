from django.urls import path
from . import views

from questions.views import custom_404_view

handler404 = custom_404_view

urlpatterns = [
    path('', views.Game_Room, name="Game_Room"),
    path('create/', views.Create_Room, name="Create_Room"),
    path('<int:room_number>/', views.Room, name="Room"),
    path('password/', views.Password_Room, name="Room_passwoed"),
    #Строку ниже удалить когда будет отлажена система разаунтификации игровой комнаты
    path('logout/<int:room_number>/',views.logout_secret, name='Logout_Secret')
]