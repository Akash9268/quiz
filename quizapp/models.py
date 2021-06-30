from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
DIFFICULT_CHOICES = (
		('1','Easy'),
		('2','Medium'),
		('3','Hard'),
)

TOPIC_CHOICES = (
		('Physics','Physics'),
		('Mathematics','Mathematics'),
		('Chemistry','Chemistry'),
		('Computer Science','Computer Science'),
		('Networking','Networking'),
)

xs
class Quiz(models.Model):
	name  = models.CharField(max_length = 100)
	topic  = models.CharField(max_length=100,choices=TOPIC_CHOICES)
	number_of_questions = models.IntegerField()
	time = models.IntegerField(help_text="Duration of the test in mins")
	required_score = models.IntegerField(help_text="required score to pass")
	difficulty = models.CharField(max_length=1,choices=DIFFICULT_CHOICES)

	def __str__(self):
		return self.name

	def get_questions(self):
		return self.questions.all()

	class Meta:
		verbose_name_plural = 'Quizes'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)
    
    def __str__(self):
        return str(self.text)

    def get_answers(self):
    	return self.answers.all()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return f"question: {self.question.text},answer:{self.text},Correct : {self.is_correct}"


class Student(models.Model):
    username = models.CharField(max_length=100,default='name')
    password = models.CharField(max_length=100,default='password')
    confirm_password = models.CharField(max_length=100,default='confirm_password')
    quizzes = models.ManyToManyField(Quiz, through='Result')
    last_login = models.DateTimeField(default=timezone.now)

    def is_active(self):
        return True

    def __str__(self):
    	return self.username

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.user)


    