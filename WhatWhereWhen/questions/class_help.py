from rest_framework.response import Response
from .models import Estimation_Quest_User
from .serializers import EstimationQuestUserSerializer
from rest_framework import generics
from rest_framework import status


class Question_Evaluation_APIView(generics.ListCreateAPIView):
    queryset = Estimation_Quest_User.objects.all()
    serializer_class = EstimationQuestUserSerializer

class Question_Evaluation_APICreate(generics.CreateAPIView):
    queryset = Estimation_Quest_User.objects.all()
    serializer_class = EstimationQuestUserSerializer


class Question_Evaluation_APIUpdate(generics.UpdateAPIView):
    queryset = Estimation_Quest_User.objects.all()
    serializer_class = EstimationQuestUserSerializer

    def get_object(self):
        user_id = self.request.data.get("user")
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

