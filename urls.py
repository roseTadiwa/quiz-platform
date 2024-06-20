from .views import take_quiz, quiz_submission
from django.contrib import admin
from django.urls import path
from . import views
from .views import save_quiz, view_quiz,submit_answer,quiz_result
urlpatterns = [
    path('', views.home, name='home'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('check-quiz/<int:quiz_id>/', views.check_quiz, name='check_quiz'),
    path('browse-quizzes/', views.browse_quizzes, name='browse_quizzes'), 
    path('take-quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),  
    path('quiz/<int:quiz_id>/', view_quiz, name='view_quiz'),
     path('submit_answer/', views.submit_answer, name='submit_answer'),    
      path('submission_result/<int:quiz_id>/', views.submission_result, name='submission_result'),   
      path('quiz/<int:quiz_id>/submit/', quiz_submission, name='quiz_submission'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
     path('save_quiz/', views.save_quiz, name='save_quiz'),   
     path('save_quiz/home.html', views.home, name='save_quiz_home'),    
          ]

