from django.utils import timezone
from datetime import timedelta

from django.core.files.images import get_image_dimensions
from .models import *
from django.core.exceptions import ValidationError
from PIL import Image
from questions.models import *



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
        # print(width, height)
    except:
        raise ValidationError('Некорректный файл')
    if width and height:
        if width > 4000 or height > 4000:  # Ограничение на размеры изображения
            raise ValidationError('Длинна или ширина изображения превышает 4000 пикселей, пожалуйста выберите другое изображение')
        # print(ValidationError)

def validate_tag(name):
    dangerous_characters = ['<', '>', '&', '/', '\\', "'", '"', ';', '\n', '\r', '?', '#', '%']
    for i in range(len(dangerous_characters)):
        if dangerous_characters[i] in name:
            raise ValidationError("Недопустимые символы в логине, пожалуйста придумайте логин без специальных символов")
    if len(name) < 3:
        raise ValidationError('Тег слишком короткий, пожалуйста придумайте тег длинной от 3 до 20 символов')
    if len(name) > 20:
        raise ValidationError('Тег слишком длинный, пожалуйста придумайте тег длинной от 3 до 20 символов')

def question_name_line_edit(name):
    if len(name) < 5:
        raise ValidationError('Название вопроса слишком короткое, пожалуйста придумайте название длинной от 5 до 50 символов')
    if len(name) > 50:
        raise ValidationError('Название вопроса слишком длинное, пожалуйста придумайте название длинной от 5 до 50 символов')




def question_name_text(name):
    estimations = Question.objects.filter(text_question=name)
    if estimations.exists():
        raise ValidationError('Вопрос с таким текстом уже существует. Пожалуйста, попробуйте сформулировать его иначе.')
    if len(name) < 20:
        # print(name)
        raise ValidationError('Текст вопроса слишком короткий, пожалуйста придумайте вопрос от 20 до 1000 символов')
    if len(name) > 1000:
        raise ValidationError('Текст вопроса слишком длинный, пожалуйста придумайте вопрос от 20 до 1000 символов')


def question_answer_text(name):
    if len(name) > 700:
        raise ValidationError('Текст примечания к ответу слишком длинный, пожалуйста придумайте примечание до 700 символов')

def Claim_text(text):
    if len(text) <10:
        raise ValidationError('Пожалуйста распишите текст жалобы подробнее (минимум 10 символов)')

def validate_tag(name):
    dangerous_characters = ['<', '>', '&', '/', '\\', ';', '\n', '\r', '#', '%']
    for i in range(len(dangerous_characters)):
        if dangerous_characters[i] in name:
            raise ValidationError("Недопустимые символы в тэге, пожалуйста придумайте тэг без специальных символов")
    if len(name) < 3:
        raise ValidationError('Тег слишком короткий, пожалуйста придумайте тег длинной от 3 до 20 символов')
    if len(name) > 20:
        raise ValidationError('Тег слишком длинный, пожалуйста придумайте тег длинной от 3 до 20 символов')

def validate_selection(name):
    dangerous_characters = ['<', '>', '&', '/', '\\', ';', '\n', '\r', '#', '%']
    for i in range(len(dangerous_characters)):
        if dangerous_characters[i] in name:
            raise ValidationError("Недопустимые символы в имени коллекции, пожалуйста придумайте имя без специальных символов")
    if len(name) < 3:
        raise ValidationError('Имя коллекции слишком короткое, пожалуйста придумайте имя длинной от 3 до 20 символов')
    if len(name) > 20:
        raise ValidationError('Имя коллекции слишком длинное, пожалуйста придумайте имя длинной от 3 до 20 символов')


from django.utils.html import escape

def chek_json_filter(data):
    search = None
    search_name = None
    search_text  = None
    search_answer = None
    checkbox_search = False
    coincidence_tag = False
    select_author = None
    unselect_author = None
    select_tag = None
    unselect_tag = None
    question_page = 0
    count_question = 5
    sorting_question = "ID"
    def chekArray(string_array):
        int_array = []
        for item in string_array:
            try:
                int_array.append(int(item))  # Пробуем преобразовать строку в целое число
            except ValueError:
                return False  # Если не удалось преобразовать, возвращаем False
        return [int_array, True]  # Возвращаем изменённый массив и True

    try:
        question_page = int(data.get('question_page'))
    except ValueError:
        pass

    try:
        count_question = int(data.get('count_question'))
    except ValueError:
        pass

    search = escape(data.get('search').strip())
    search_name = escape(data.get('search_name').strip())
    search_text = escape(data.get('search_text').strip())
    search_answer = escape(data.get('search_answer').strip())


    if data.get('coincidence_tag') == True or data.get('coincidence_tag') == False:
        coincidence_tag = data.get('coincidence_tag')

    if data.get('checkbox_search') == True or data.get('checkbox_search') == False:
        checkbox_search = data.get('checkbox_search')

    array = chekArray(data.get('select_author'))
    if array:
        select_author = array[0]

    array = chekArray(data.get('unselect_author'))
    if array:
        unselect_author = array[0]

    array = chekArray(data.get('select_tag'))
    if array:
        select_tag = array[0]

    array = chekArray(data.get('unselect_tag'))
    if array:
        unselect_tag = array[0]

    sorting_question_test = data.get('sorting_question')
    if sorting_question_test ==  "average_estimation":
        sorting_question = "average_estimation"
    elif sorting_question_test == "-average_estimation":
        sorting_question = "-average_estimation"
    elif sorting_question_test == "-ID":
        sorting_question = "-ID"
    else:
        sorting_question = "ID"




    data_get = {
        "search": search,
        "search_name": search_name,
        "search_text": search_text,
        "search_answer": search_answer,
        "checkbox_search":checkbox_search,
        "coincidence_tag": coincidence_tag,
        "select_author": select_author,
        "unselect_author": unselect_author,
        "select_tag": select_tag,
        "unselect_tag": unselect_tag,
        "question_page": question_page,
        "count_question": count_question,
        "sorting_question":sorting_question,
    };
    return data_get

def average_score(question):
    Estimation = Estimation_Quest_User.objects.filter(question=question)
    score=0
    for Est in Estimation:
        score+=Est.estimation
    if score !=0:
        question_score=round(score/len(Estimation), 1)
    else:
        question_score = 0.0

    return question_score