from django.contrib import admin
from .models import *

admin.site.register(Licenses)
admin.site.register(Question)
admin.site.register(Estimation_Quest_User)
admin.site.register(Tags)
admin.site.register(Tags_Questions)
admin.site.register(Selections)
admin.site.register(Selection_Questions)
admin.site.register(Complaints_Questions)
admin.site.register(Complaints_Selections)

