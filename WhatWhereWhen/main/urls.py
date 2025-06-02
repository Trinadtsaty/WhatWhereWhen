from django.urls import path
from . import views

from questions.views import custom_404_view

handler404 = custom_404_view

urlpatterns = [
    path('', views.Game_Room, name="Game_Room"),
    path('create', views.Create_Room, name="Create_Room"),
]