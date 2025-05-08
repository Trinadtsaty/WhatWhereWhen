from django.urls import path
from . import views
from .views import Question_Evaluation_APIView



urlpatterns = [
    path('', views.question_main, name="Question_Room"),
    path('add/', views.question_add, name="Question_add"),
    path('<int:question_number>/', views.question, name="Question"),
    path('api/v1',Question_Evaluation_APIView.as_view())
]