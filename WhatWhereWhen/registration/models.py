from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
    login = models.CharField(max_length=50)
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
    online = models.BooleanField(default=False)
    # Является ли пользователь разработчиком
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
    id = models.BigAutoField( primary_key=True)
    #Звание
    titles_name = models.CharField( max_length=50, unique=True)
    #Описание
    titles_description = models.TextField()

    def __str__(self):
        return self.titles_name

    class Meta:
        verbose_name = 'Звание'
        verbose_name_plural = 'Звания'


class Users_and_Titles(models.Model):
    # id юнита
    id = models.BigAutoField(primary_key=True)
    # Пользователь
    users = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='Users')
    # Звание
    titles_units = models.ForeignKey(Titles, on_delete=models.CASCADE, related_name='Titles')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'
