from rest_framework import serializers
from .models import Estimation_Quest_User

from .models import Question
from registration.models import Users

# class EstimationQuestUserSerializer(serializers.Serializer):
#     question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
#     users = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
#     estimation = serializers.IntegerField()

class EstimationQuestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimation_Quest_User
        fields = '__all__'