from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.question_main, name="Question_Room"),
    path('add/', views.question_add, name="Question_add"),
    path('<int:question_number>/', views.question, name="Question"),
    path('tag/', views.tag_add, name="Tag_add"),
    path('api/v1', Question_Evaluation_API.as_view()),
    path('api/v2', Tag_Question_API.as_view()),

]