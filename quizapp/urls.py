from django.urls import path
from .views import QuizListView,quiz_view,QuizDeleteView
from quizapp import views

app_name = 'quizes'

urlpatterns = [
    path('main/',QuizListView.as_view(),name='main-detail'),
    path('main/<int:pk>/',views.quiz_view,name='quiz-start'),
    path('main/cc/create',views.create_form,name='create-form'),
    path('main/<int:pk>/delete',QuizDeleteView.as_view(),name='delete-record'), 
    path('main/<int:pk>/detail',views.quiz_detail_view,name='quiz-detail'),
    path('main/<int:pk>/ques',views.create_question,name='ques-form'),
    path('main/signin/sign_up',views.signup,name='signup'),
    path('main/<int:pk>/<int:pk2>/ques/ans',views.create_answer,name='ans-form'),
    path('main/login/',views.studentlogin,name='login'),
    path('main/quiz-list/',views.quiz_list,name='quiz-list'),
    path('main/<int:pk>/data/',views.take_quiz,name='take-quiz'),
    path('main/<int:pk>/save/',views.save_quiz,name='save-quiz'),
    path('main/logout/',views.studentlogout,name='logout'),

]