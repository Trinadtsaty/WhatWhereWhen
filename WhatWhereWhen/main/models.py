from django.db import models
from questions.models import Selections
from registration.models import Users
from django.core.validators import MinValueValidator, MaxValueValidator

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
    password_room = models.CharField(max_length=50)
    selections = models.ForeignKey(Selections, on_delete=models.PROTECT, related_name='Selection_Author')
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





