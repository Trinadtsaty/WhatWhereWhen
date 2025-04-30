# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from .models import Users
# import datetime
# import os
#
#
# @receiver(pre_save, sender=Users)
# def change_file_name(sender, instance, **kwargs):
#     if instance.picture:
#         print("1 instance.picture.url=", instance.picture.url)
#         print("1 instance.picture.name=", instance.picture.name)
#
#         # Получаем расширение файла
#         file_extension = instance.picture.name.split('.')[-1]
#
#         # Формируем новое имя файла без дублирования пути
#         new_file_name = f"IMG/Users/{datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}_{instance.ID}.{file_extension}"
#
#         # Устанавливаем новое имя файла
#         instance.picture.name = new_file_name
#         print("2 instance.picture.url=", instance.picture.url)
#         print("2 instance.picture.name=", instance.picture.name)