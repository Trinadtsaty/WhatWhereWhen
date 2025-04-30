from django.urls import path
from . import views

urlpatterns = [
    path('', views.Question_main, name="Question_Room"),
]