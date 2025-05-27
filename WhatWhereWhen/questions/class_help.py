from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework import status


# class Question_Evaluation_APIView(generics.ListCreateAPIView):
#     queryset = Estimation_Quest_User.objects.all()
#     serializer_class = EstimationQuestUserSerializer

# Оценки:
class Question_Evaluation_APICreate(generics.CreateAPIView):
    queryset = Estimation_Quest_User.objects.all()
    serializer_class = EstimationQuestUserSerializer

class Question_Evaluation_APIUpdate(generics.UpdateAPIView):
    queryset = Estimation_Quest_User.objects.all()
    serializer_class = EstimationQuestUserSerializer

    def get_object(self):
        # user_id = self.request.data.get("user")
        user_id = self.request.user
        question_id = self.request.data.get("question")

        if not user_id:
            self._raise_error("PUT is not user")
        if not question_id:
            self._raise_error("PUT is not question")

        try:
            return Estimation_Quest_User.objects.get(user=user_id, question=question_id)
        except Estimation_Quest_User.DoesNotExist:
            self._raise_error("Объекта нет")

    def _raise_error(self, message):
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


#Связь тегов и вопросов
class Tag_Question_APICreate(generics.CreateAPIView):
    queryset = Tags_Questions.objects.all()
    serializer_class = TagsQuestionSerializer


#Связь Подборок и вопросов
class Selection_Questions_APICreate(generics.CreateAPIView):
    queryset = Selection_Questions.objects.all()
    serializer_class = SelectionQuestionsSerializer

    def _raise_error(self, message):
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

class Selection_Questions_APIDestroy(generics.DestroyAPIView):
    queryset = Selection_Questions.objects.all()
    serializer_class = SelectionQuestionsSerializer

    def get_object(self):
        selection_id = self.request.data.get("selection_id")
        question_id = self.request.data.get("question_id")

        if not selection_id:
            self._raise_error("DELETE is not selection")
        if not question_id:
            self._raise_error("DELETE is not question")

        try:
            return Selection_Questions.objects.get(selection_id=selection_id, question_id=question_id)
        except Estimation_Quest_User.DoesNotExist:
            self._raise_error("Объекта нет")

    def _raise_error(self, message):
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView


class SelectionsByQuestionAPIView(APIView):

    def get(self, request, question_id):
        # Проверяем, существует ли question_id
        if not question_id:
            return self._raise_error("Отсутствует question_id")

        try:
            # Получаем все связи по question_id
            selection_questions = Selection_Questions.objects.filter(question_id=question_id)
            # Получаем все уникальные подборки
            selections = Selections.objects.filter(
                ID__in=selection_questions.values_list('selection_id', flat=True),
                selection_author=request.user
            )

            serializer = SelectionsSerializer(selections, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Selection_Questions.DoesNotExist:
            return self._raise_error("Объекта нет")

    def _raise_error(self, message):
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, question_id):
    #     # Получаем все связи по question_id
    #     selection_questions = Selection_Questions.objects.filter(question_id=question_id)
    #
    #     # Получаем все уникальные подборки
    #     selections = Selections.objects.filter(ID__in=selection_questions.values_list('selection_id', flat=True), selection_author=request.user)
    #
    #     serializer = SelectionsSerializer(selections, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
# Вопросы
# class Question_APIView(generics.ListCreateAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#
# class Question_APICreate(generics.CreateAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#
# class Question_APIUpdate(generics.UpdateAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#
#     def get_object(self):
#         question_id = self.request.data.get("ID")
#
#         if not question_id:
#             self._raise_error("PUT is not question")
#
#         try:
#             return Question.objects.get(ID=question_id)
#         except Question.DoesNotExist:
#             self._raise_error("Объекта нет")
#
#     def _raise_error(self, message):
#         return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)




