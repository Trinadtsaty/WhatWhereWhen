from django.shortcuts import redirect
from functools import wraps
from .models import Question
from django.http import Http404

def edit_question(view_func):
    @wraps(view_func)
    def _wrapped_view(request, question_number, *args, **kwargs):
        # Проверка на аутентификацию пользователя
        if not request.user.is_authenticated:
            return redirect('Login')

        try:
            question = Question.objects.get(ID=int(question_number))
        except Question.DoesNotExist:
            # Обработка случая, когда вопрос не найден
            raise Http404("Страница не найдена")  # Замените 'some_redirect_url' на ваш URL

        if request.user != question.question_author:
            raise Http404("Страница не найдена")  # Замените 'some_redirect_url' на ваш URL

        return view_func(request, question_number, *args, **kwargs)  # Передаем question в view_func

    return _wrapped_view
