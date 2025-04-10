from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name="Menu"),
    path("login", views.login, name="Login"),
    path("register", views.register, name="Register")
]