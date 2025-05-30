from django.urls import path
from . import views
from .views import *

from .views import custom_404_view

handler404 = custom_404_view

urlpatterns = [
    path('', views.question_main, name="Question_Room"),
    path('selection', views.selection, name="Selection_Room"),
    path('add/', views.question_add, name="Question_add"),
    path('<int:question_number>/', views.question, name="Question"),
    path('tag/', views.tag_add, name="Tag_add"),
    path('questionclaim/<int:question_number>/',  views.questionClaim, name="Claim_Question"),
    path('selectionClaim/',  views.selectionClaim, name="Claim_Tag"),
    path('selection/',  views.selectionCreate, name="Selection_Create"),
    path('<int:question_number>/edit/', views.question_edit, name="Question_Edit"),
    path('api/v1', Question_Evaluation_API.as_view()),
    path('api/v2', Tag_Question_API.as_view()),
    path('api/v3', Selection_Questions_API.as_view()),
    path('api/v4/<int:question_id>/', Selection_API.as_view()),
]

