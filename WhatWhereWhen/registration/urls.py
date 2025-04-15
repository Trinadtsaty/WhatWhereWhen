from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name="Menu"),
    path("login", views.user_login, name="Login"),
    path("register", views.user_register, name="Register")
]