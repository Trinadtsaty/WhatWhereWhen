from django.contrib import admin
from .models import * #Импортируем все модели

admin.site.register(Users)
admin.site.register(Titles)
admin.site.register(Users_and_Titles)