from rest_framework import serializers
from .models import Estimation_Quest_User

class EstimationQuestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimation_Quest_User
        fields = '__all__'
