from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import os
import datetime


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле электронной почты должно быть задано')
        if not password:
            raise ValueError('Пароль должен быть задан')
        email = email.lower()
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_root', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    # id игрока
    ID = models.BigAutoField(primary_key=True)
    # Логин игрока
    login = models.CharField(max_length=20)
    # мыло игрока
    email = models.EmailField(max_length=150, unique=True)
    # Картинка профиля
    picture = models.ImageField(upload_to='IMG/Users', blank=True, null=True)
    # сыграл всего игр
    played_games = models.BigIntegerField(default=0)
    # Был ведущим в стольких играх
    leader_games = models.BigIntegerField(default=0)
    # Победил в играх
    win_games = models.BigIntegerField(default=0)
    #admin@example.com

    # Активен ли пользователь сейчас
    is_active = models.BooleanField(default=True)
    # Активен ли пользователь сейчас
    last_activity = models.DateTimeField(default=timezone.now)
    # Является ли пользователь разработчиком убрать при следующей обновлении
    is_root = models.BooleanField(default=False)
    # Является ли пользователь модератором
    is_moder = models.BooleanField(default=False)
    # Является ли пользователь администратором
    is_admin = models.BooleanField(default=False)

    #заменить на is_root при настройки админки и переписать БД
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Titles(models.Model):
    #id звания
    ID = models.BigAutoField( primary_key=True)
    #Звание
    titles_name = models.CharField( max_length=20, unique=True)
    #Описание
    titles_description = models.TextField()


    def __str__(self):
        return self.titles_name

    class Meta:
        verbose_name = 'Звание'
        verbose_name_plural = 'Звания'


class Users_and_Titles(models.Model):
    # id юнита
    ID = models.BigAutoField(primary_key=True)
    # Пользователь
    users = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='Users')
    # Звание
    titles = models.ForeignKey(Titles, on_delete=models.CASCADE, related_name='Titles')
    # Время получения
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return str(self.ID)
        return str(self.users.email[:7] + "..." + " " + self.titles.titles_name[:5] + "...")

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'

class Message(models.Model):
    ID = models.BigAutoField(primary_key=True)
    users_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='Users_Recipient')
    letter_name = models.CharField(max_length=50)
    letter_text = models.TextField()

    publication = models.BooleanField(default=True)
    sender = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Sender_Letter', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.letter_name

    class Meta:
        verbose_name = 'Послание'
        verbose_name_plural = 'Послания'
