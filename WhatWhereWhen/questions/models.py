from django.db import models
from registration.models import Users
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Question(models.Model):
    # name
    # description
    # answer
    # licens
    ID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Estimation_Quest_User(models.Model):
    ID = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='Question')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='Users_Question')
    estimation = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    def __str__(self):
        return str(self.user.email)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        unique_together = ('user', 'question')