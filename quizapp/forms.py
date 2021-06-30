from .models import Quiz,Question,Answer,Student
from django import forms
from django.forms import ModelForm
from django.forms.utils import ValidationError
from django.forms.models import BaseInlineFormSet
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.forms import  AuthenticationForm



class QuizForm(ModelForm):
	class Meta():
		model = Quiz
		fields = "__all__"
		

class QuestionForm(ModelForm):
    class Meta():
        model = Question
        fields = ('text', )

class AnswerForm(ModelForm):
	class Meta():
		model = Answer
		fields = ('text','is_correct')


class LoginForm(AuthenticationForm):

    class Meta:
        model = Student
        fields=['username','password']
        username = forms.CharField()
        widgets ={'password': forms.PasswordInput}


class signupForm(ModelForm):
    
    class Meta:
        model = Student
        fields = ['username','password','confirm_password']
        widgets = {'password': forms.PasswordInput, 'confirm_password': forms.PasswordInput}
        username = forms.CharField(max_length=100)

# class BaseAnswerInlineFormSet(BaseInlineFormSet):
#     def clean(self):
#         super().clean()

#         has_one_correct_answer = False
#         for form in self.forms:
#             if not form.cleaned_data.get('DELETE', False):
#                 if form.cleaned_data.get('is_correct', False):
#                     has_one_correct_answer = True
#                     break
#         if not has_one_correct_answer:   
#             raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')