from django.db import models
from registration.models import Users
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
#admin@example.com
class Licenses(models.Model):
    ID = models.BigAutoField(primary_key=True)
    license_name = models.CharField(max_length=50)
    license_description = models.TextField()

    license_adder = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='License_Adder')
    publication = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    verified_admin = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Verified_License_Admin', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.license_name

    class Meta:
        verbose_name = 'Лицензия'
        verbose_name_plural = 'Лицензии'

class Question(models.Model):
    ID = models.BigAutoField(primary_key=True)
    question_name = models.CharField(max_length=150)
    text_question = models.TextField()
    note = models.TextField(null=True, blank=True)
    answer = models.CharField(max_length=150)
    answer_description = models.TextField(null=True, blank=True)
    license_id = models.ForeignKey(Licenses, on_delete=models.PROTECT, related_name='License', null=True, blank=True)

    question_author = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Question_Author')
    publication = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    verified_admin = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Verified_Question_Admin', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_name

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Estimation_Quest_User(models.Model):
    ID = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='Question')
    user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='User_Question')
    estimation = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    def __str__(self):
        return str(self.user.email[:7] + "..." + " " + self.question.question_name[:5] + "...")

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        unique_together = ('user', 'question')
""
class Tags(models.Model):
    ID = models.BigAutoField(primary_key=True)
    tag_name = models.CharField(max_length=50)

    tag_author = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Tag_Author')
    publication = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    verified_admin = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Verified_Tag_Admin', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Tags_Questions(models.Model):
    ID = models.BigAutoField(primary_key=True)
    tags_id = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name='Tag')
    question_id = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='Question_Tag')

    tag_adder = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Tag_Adder')
    publication = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    verified_admin = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Verified_Tag_Question_Admin', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.tags_id.tag_name[:5] + "..." + " " + self.question_id.question_name[:5] + "...")

    class Meta:
        verbose_name = 'Связь Тега с вопросом'
        verbose_name_plural = 'Связи Тегов с вопросами'
        unique_together = ('tags_id', 'question_id')

class Selections(models.Model):
    ID = models.BigAutoField(primary_key=True)
    selection_name = models.CharField(max_length=50)
    private = models.BooleanField(default=False)

    selection_author = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Selection_Author')
    publication = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    verified_admin = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Verified_Selection_Admin', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.selection_name

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

class Selection_Questions(models.Model):
    ID = models.BigAutoField(primary_key=True)
    selection_id = models.ForeignKey(Selections, on_delete=models.CASCADE, related_name='Selection')
    question_id = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='Question_Select')

    publication = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    verified_admin = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Verified_Selection_Question_Admin', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.selection_id.selection_name[:5] + "..." + " " + self.question_id.question_name[:5] + "...")

    class Meta:
        verbose_name = 'Связь Вопрос Подборка'
        verbose_name_plural = 'Связи Вопросов и Подборок'
        unique_together = ('selection_id', 'question_id')

class Complaints_Questions(models.Model):
    ID = models.BigAutoField(primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='Question_Complaint')
    complaint_name = models.CharField(max_length=150)
    complaint_description = models.TextField()

    complaint_author = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Complaint_Question_Author')
    verified = models.BooleanField(default=False)
    verified_admin = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Verified_Complaint_Question_Admin', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.complaint_name

    class Meta:
        verbose_name = 'Жалоба на вопрос'
        verbose_name_plural = 'Жалобы на вопросы'

class Complaints_Selections(models.Model):
    ID = models.BigAutoField(primary_key=True)
    selections_id = models.ForeignKey(Selections, on_delete=models.PROTECT, related_name='Selection_Complaint')
    complaint_name = models.CharField(max_length=150)
    complaint_description = models.TextField()

    complaint_author = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Complaint_Selection_Author')
    verified = models.BooleanField(default=False)
    verified_admin = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='Verified_Complaint_Selection_Admin', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.complaint_name

    class Meta:
        verbose_name = 'Жалоба на подборку'
        verbose_name_plural = 'Жалобы на Подборки'