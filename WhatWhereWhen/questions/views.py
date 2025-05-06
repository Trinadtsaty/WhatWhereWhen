from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.



def question_main(request):
    # return render(request, "questions/question_main.html")
    title = 'Вопросы'
    return render(request, "questions/pattern.html", {"title" : title})


@login_required()
def question_add(request):
    return render(request, "questions/question_add.html")


def question(request,question_number):
    tegs=['тег 1', 'тег 2', 'тег 3', 'тееееееееееег 4' ]
    question_text = "Текст вопроса"
    question_name = f"Вопрос номер {question_number}"
    note ="примичание"
    answer_not = "Описание овтета"
    answer = "ответ"
    estimation_ball=6.3
    estimation_ball_bol=False
    my_estimation=3
    license_name = "MIT License/X11 License"
    license_text = """
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""



    return render(request, "questions/question.html", {
        "number" : question_number,
        "title" : 'Страница вопроса',
        "tegs" : tegs,
        "question_name": question_name,
        "question_text": question_text,
        "note" : note,
        "answer" : answer,
        "license_name" : license_name,
        "license_text" : license_text,
        "answer_not":answer_not,
        "estimation_ball": estimation_ball,
        "estimation_ball_bol": estimation_ball_bol,
        "my_estimation": my_estimation,
    })
