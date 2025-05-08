from rest_framework import serializers
from .models import Estimation_Quest_User

class EstimationQuestUserSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Estimation_Quest_User
        # fields = '__all__'
        fields = ("question", "user", "estimation")
