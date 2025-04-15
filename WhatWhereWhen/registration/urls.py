from django.urls import path
from .views import custom_logout
from . import views

urlpatterns = [
    path('', views.menu, name="Menu"),
    path("login", views.user_login, name="Login"),
    path("register", views.user_register, name="Register"),
    path('logout/', custom_logout, name="Log_Out")
]