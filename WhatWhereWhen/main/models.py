from django.db import models
from questions.models import Selections
from registration.models import Users
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
#admin@example.com

class game_rooms(models.Model):
    Game_mode = [
        (0, 'Классика'),
        (1, 'Спорт'),
        (2, 'Совместный ответ'),
    ]

    ID = models.BigAutoField(primary_key=True)
    room_name = models.CharField(max_length=50)
    clos_room = models.BooleanField(default=False)
    password_room = models.CharField(max_length=50, null=True, blank=True)
    selections = models.ForeignKey(Selections, on_delete=models.PROTECT, related_name='Selection_Room')
    game_mode = models.IntegerField(choices=Game_mode, default=0)
    host = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='host_game_rooms')
    captain =models.ForeignKey(Users, on_delete=models.PROTECT, related_name='captain_game_rooms', null=True, blank=True)
    leader = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='leader_game_rooms', null=True, blank=True)
    room_limit = models.IntegerField(
        validators=[
            MinValueValidator(3),
            MaxValueValidator(8)
        ]
    )
    people_on_page = models.JSONField(default=dict, null=True, blank=True)
    room_description = models.TextField(null=True, blank=True)
    early_answer = models.BooleanField(default=True)
    time_answer = models.IntegerField(
        validators=[
            MinValueValidator(5),
            MaxValueValidator(600)
        ]
    )
    clear_chat = models.BooleanField(default=False)
    question_time = models.IntegerField(
        validators=[
            MinValueValidator(10),
            MaxValueValidator(600)
        ]
    )
    show_question = models.BooleanField(default=True)
    reading_speed = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(60)
        ]
    )
    random_order = models.BooleanField(default=True)
    break_between_questions = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(600)
        ]
    )

    def clean(self):
        super().clean()
        if self.clos_room and not self.password_room:
            raise ValidationError({'password_room': 'Это поле обязательно, если clos_room установлено в True.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызываем clean перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return self.room_name

    class Meta:
        verbose_name = 'Игровая комната'
        verbose_name_plural = 'Игровые комнаты'
