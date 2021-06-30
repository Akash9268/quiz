from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.urls import reverse_lazy
from .models import Quiz,Question,Answer,Student,Result
from .forms import QuizForm,QuestionForm,AnswerForm,LoginForm,signupForm
from django.views.generic import (TemplateView,ListView,
									DetailView,CreateView,
									UpdateView,DeleteView)# Create your views here.
from django.forms import inlineformset_factory
from django.db import transaction
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def studentlogout(request):
    logout(request)
    return render(request, 'quizapp/main.html')

def signup(request):
    if request.method == 'GET':
        form = signupForm()
        return render(request, 'registeration/signup_form.html', {'form': form})
    else:
        form = signupForm(request.POST)
        if form.is_valid():
            pass1 = form.cleaned_data["password"]
            pass2 = form.cleaned_data["confirm_password"]
            if pass1 != pass2:
                messages.warning(
                    request, 'The two password fields do not match')
                return render(request, 'registeration/signup_form.html', {'form': form})
            form.save()
            return render(request,'quizapp/main.html')
        return render(request, 'registeration/signup_form.html', {'form': form})

def quiz_list(request):
	quiz = Quiz.objects.all()
	return render(request,'quizapp/quiz_list.html',{'quizes':quiz})

def home(request):
	return render(request,'quizapp/main.html')

class QuizListView(ListView):
	model = Quiz
	template_name = 'quizapp/main2.html'

class QuizDeleteView(DeleteView):
	model = Quiz
	success_url = reverse_lazy('quizes:main-detail')
		
def quiz_view(request,pk):
	quiz = get_object_or_404(Quiz,pk=pk)
	return render(request,'quizapp/quiz.html',{'quiz':quiz})

def quiz_detail_view(request,pk):
	quiz = get_object_or_404(Quiz,pk =pk)
	print(quiz.questions.all().values())
	return render(request,'quizapp/quiz_detail.html',{'quiz':quiz})

def create_form(request):
	if request.method == 'POST':
		form = QuizForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('quizes:main-detail')

	else:
		form = QuizForm()

	return render(request,'quizapp/quiz_form.html',{'form':form})


def create_question(request,pk):
	quizz = get_object_or_404(Quiz,pk=pk)
	if request.method == 'POST':
		form2 = QuestionForm(request.POST)
		if form2.is_valid():
			question = form2.save(commit=False)
			question.quiz = quizz
			form2.save()	
			return redirect('quizes:quiz-detail',pk = quizz.pk)

	else:
		form2 = QuestionForm()

	return render(request,'quizapp/create_questions.html',{'form':form2,'quiz':quizz})

def create_answer(request,pk,pk2):
	quiz = get_object_or_404(Quiz,pk=pk2)
	question = get_object_or_404(Question,pk=pk,quiz=quiz)
	AnswerFormSet = inlineformset_factory(Question,Answer,fields = ('text','is_correct'),min_num=4,
        validate_min=True,
        max_num=4,
        validate_max=True)


	if request.method == 'POST':
		form1 = QuestionForm(request.POST,instance=question)
		formset = AnswerFormSet(request.POST,instance=question)
		if form1.is_valid() and formset.is_valid():
			with transaction.atomic():
				form1.save()
				formset.save()	
			return redirect('quizes:quiz-detail',pk = pk2)

		else:
			return HttpResponse("not is_valid")


	else:
		formset = AnswerFormSet(instance=question)
		form1 = QuestionForm(instance=question)

	return render(request,'quizapp/create_answers.html',{'formset':formset,'questionform':form1,'question':question,'quiz':quiz})


def studentlogin(request):
    if request.method == "POST":
        fm = LoginForm(request, data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data["username"]
            passw = fm.cleaned_data["password"]
            student = Student.objects.filter(username=username).first()
            if student is not None:
                if student.password == passw:
                    login(request,student,
                          backend='quizapp.loginbackend.StudentAuthBackend')
                    quiz = Quiz.objects.all()

                    global val
                    def val():
                    	return student

                    return render(request, 'quizapp/quiz_list.html',{'quizes':quiz})
                else:
                    messages.warning("Invalid username or password")
                    return render(request, 'registeration/login.html', context)
    else:
        fm = LoginForm()
    return render(request, 'registeration/login.html', {'form': fm})


def take_quiz(request,pk):
	quiz = get_object_or_404(Quiz,pk=pk)
	questions = []
	for q in quiz.get_questions():
		options = []
		for a in q.get_answers():
			options.append(a.text)
		questions.append({str(q):options})

	return JsonResponse({
		'data':questions,
		'time':quiz.time,
		})


def save_quiz(request,pk):
	user = val()
	if request.is_ajax():
		questions = []
		data = request.POST
		data_ = dict(data.lists())
		data_.pop('csrfmiddlewaretoken')

		for k in data_.keys():
			question  = Question.objects.get(text=k)
			questions.append(question)

		quiz = get_object_or_404(Quiz,pk=pk)

		score = 0
		multiplier = 100/quiz.number_of_questions
		results = []	
		correct_answer = None

		for q in questions:
			a_selected = request.POST.get(q.text)
			if a_selected != "":
				question_answer = Answer.objects.filter(question=q)
				for a in question_answer:
					if a_selected == a.text:
						if a.is_correct:
							score += 1
							correct_answer = a.text
					else:
						if a.is_correct:
							correct_answer = a.text

				results.append({str(q):{'correct_answer':correct_answer,'answered':a_selected}})

			else:
				results.append({str(q):'not_answered'})


		score_ = score*multiplier
		Result.objects.create(quiz=quiz,user=user,score=score_)

		if score_ >= quiz.required_score:
			return JsonResponse({"passed":True,'score':score_,'results':results})
		else:
			return JsonResponse({"passed":False,'score':score_,'results':results})
