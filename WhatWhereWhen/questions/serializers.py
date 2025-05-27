from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError

class EstimationQuestUserSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Estimation_Quest_User
        fields = ("question", "user", "estimation")

class TagsQuestionSerializer(serializers.ModelSerializer):
    tag_adder = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Tags_Questions
        fields = ("tags_id", "question_id", "tag_adder")

class SelectionQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection_Questions
        fields = ("selection_id", "question_id")

    def validate(self, data):

        selection_id = data.get('selection_id').ID
        print("тип поля selection_id",type(selection_id))
        print(selection_id)
        user = self.context['request'].user
        if selection_id:
            try:
                selection = Selections.objects.get(ID=selection_id)
                print(selection.selection_author)
                print(user)
                if selection.selection_author != user:
                    raise ValidationError("Вы не имеете прав на добавление вопросов в этот выбор.")
            except Selections.DoesNotExist:
                raise ValidationError("Выбор с данным ID не существует.")
        return data



# class SelectionsSerializer(serializers.ModelSerializer):
#     selection_author = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     class Meta:
#         model = Selections
#         fields = ("selection_name", "private", "selection_author")


# class LicensesSerializer(serializers.ModelSerializer):
#     license_adder = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     class Meta:
#         model = Licenses
#         fields = ("license_name", "license_description", "license_adder")

# class QuestionSerializer(serializers.ModelSerializer):
#     question_author = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     class Meta:
#         model = Question
#         fields = ("question_name", "text_question", "note", "answer", "answer_description", "license_id", "question_author")

# class TagsSerializer(serializers.ModelSerializer):
#     tag_adder = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     class Meta:
#         model = Tags
#         fields = ("tag_name", "tag_adder")

# class SelectionsSerializer(serializers.ModelSerializer):
#     selection_author = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     class Meta:
#         model = Selections
#         fields = ("selection_name", "private", "selection_author")

# class ComplaintsQuestionsSerializer(serializers.ModelSerializer):
#     complaint_author = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     class Meta:
#         model = Complaints_Questions
#         fields = ("question_id", "complaint_name", "complaint_description","complaint_author")

# class ComplaintsQuestionsSerializer(serializers.ModelSerializer):
#     complaint_author = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     class Meta:
#         model = Complaints_Selections
#         fields = ("question_id", "complaint_name", "complaint_description","complaint_author")