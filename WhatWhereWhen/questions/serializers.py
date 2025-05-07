import io

from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Titles





class TitleSerializer(serializers.Serializer):
    #название полей (titles_name и titles_description) должны совпадать с соответсвующими полями в TitlesModel
    titles_name = serializers.CharField(max_length=20)
    titles_description = serializers.CharField()



# class TitlesModel:
#     def __init__(self, titles_name, titles_description):
#         self.titles_name = titles_name
#         self.titles_description = titles_description





# def encode():
#     model = TitlesModel('Побудитель по жизни', 'Победить в 10 играх подрят')
#     model_sr = TitleSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# def decode():
#     stream = io.BytesIO(b'{"titles_name":"Тестовая запись","titles_description":"Эта запись создана для тестирования"}')
#     data = JSONParser().parse(stream)
#     serializer = TitleSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)