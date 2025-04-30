from django.urls import path
from . import views

urlpatterns = [
    path('', views.Game_Room, name="Game_Room")
]