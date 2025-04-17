from django.utils import timezone
from datetime import timedelta
from .models import Users

from django.core.files.images import get_image_dimensions
from .models import Users
from django.core.exceptions import ValidationError
from PIL import Image

def get_active_users():
    # Определяем временной порог для активности пользователей
    time_threshold = timezone.now() - timedelta(minutes=5)
    # Возвращаем количество пользователей, активных в последние 5 минут
    return Users.objects.filter(last_activity__gte=time_threshold).count()

def validate_email(email):
    dangerous_characters = ['<', '>', '&', '/', '\\', "'", '"', ';', ' ', '\n', '\r', '?', '#', '%']
    for i in range(len(dangerous_characters)):
        if dangerous_characters[i] in email:
            raise ValidationError("Недопустимые символы в электронной почте, пожалуйста введите корректную почту")

    if Users.objects.filter(email=email).exists():
        raise ValidationError('Данная почта уже зарегистрирована, пожалуйста воспользуйтесь функцией "Восстановление пароля"')

def validate_email_login(email):
    dangerous_characters = ['<', '>', '&', '/', '\\', "'", '"', ';', ' ', '\n', '\r', '?', '#', '%']
    for i in range(len(dangerous_characters)):
        if dangerous_characters[i] in email:
            raise ValidationError("Недопустимые символы в электронной почте, пожалуйста введите корректную почту")

def validate_name(name):
    dangerous_characters = ['<', '>', '&', '/', '\\', "'", '"', ';', ' ', '\n', '\r', '?', '#', '%']
    for i in range(len(dangerous_characters)):
        if dangerous_characters[i] in name:
            raise ValidationError("Недопустимые символы в логине, пожалуйста придумайте логин без специальных символов")
    if len(name) < 3:
        raise ValidationError('Ник слишком короткий, пожалуйста придумайте ник длинной от 3 до 20 символов')
    if len(name) > 20:
        raise ValidationError('Ник слишком длинный, пожалуйста придумайте ник длинной от 3 до 20 символов')


def validate_password(password):
    dangerous_characters = ['<', '>', '&', '/', '\\', "'", '"', ';', ' ', '\n', '\r', '?', '#', '%']
    for i in range(len(dangerous_characters)):
        if dangerous_characters[i] in password:
            raise ValidationError("Недопустимые символы в пароле, пожалуйста придумайте пароль без специальных символов")

    if len(password) < 8:
        raise ValidationError('Пароль слишком короткий, пожалуйста придумайте пароль длинной от 8 до 30 символов')

    if len(password) > 30:
        raise ValidationError('Пароль слишком длинный, пожалуйста придумайте пароль длинной от 8 до 30 символов')

def validate_password_login(password):
    dangerous_characters = ['<', '>', '&', '/', '\\', "'", '"', ';', ' ', '\n', '\r', '?', '#', '%']
    for i in range(len(dangerous_characters)):
        if dangerous_characters[i] in password:
            raise ValidationError("Недопустимые символы в пароле, пожалуйста придумайте пароль без специальных символов")

def validate_image(image):
    # Проверка типа файла
    if not image.name.endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError('Неверный формат изображения, пожалуйста выберите изображение расширения  ".png", ".jpg" или ".jpeg"')
    try:
        with Image.open(image) as img:
            img.verify()  # Проверяет, является ли изображение корректным
    except (IOError, SyntaxError):
        raise ValidationError('Изображение повреждено, пожалуйста попробуйте загрузить другое изображение')

        # Проверка размера файла (например, не более 5MB)
    if image.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError('Изображение весит более 5Мбайт, пожалуйста загрузите иное изображение')
    try:
        width, height = get_image_dimensions(image)
        print(width, height)
    except:
        raise ValidationError('Некорректный файл')
    if width and height:
        if width > 4000 or height > 4000:  # Ограничение на размеры изображения
            raise ValidationError('Длинна или ширина изображения превышает 4000 пикселей, пожалуйста выберите другое изображение')
        print(ValidationError)

