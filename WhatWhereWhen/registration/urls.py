from django.urls import path
from .views import custom_logout, Users_mainAPI
from . import views

urlpatterns = [
    path('', views.menu, name="Menu"),
    path("login/", views.user_login, name="Login"),
    path("register/", views.user_register, name="Register"),
    path('logout/', custom_logout, name="Log_Out"),
    path('usersmain/', Users_mainAPI.as_view(), name="Users_mainAPI"),
    path('change/', views.change_profile, name="Change"),
    path('hint/', views.hint, name="Hint"),
    path('author/', views.author, name="Author"),
]


