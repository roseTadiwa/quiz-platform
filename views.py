from django.shortcuts import render,redirect
from .models import Quiz, Question, Option, Submission
from django.utils.safestring import mark_safe
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def create_quiz(request):
    if request.method == 'POST':
        quiz_title = request.POST.get('quiz_title')
        question_count = int(request.POST.get('question_count'))

        quiz = Quiz.objects.create(title=quiz_title)

        for i in range(1, question_count + 1):
            question_text = request.POST.get(f'question_{i}')
            option1_text = request.POST.get(f'option_{i}_1')
            option2_text = request.POST.get(f'option_{i}_2')

            question = Question.objects.create(quiz=quiz, text=question_text)

            option1 = Option.objects.create(question=question, text=option1_text)
            option2 = Option.objects.create(question=question, text=option2_text)

            # Additional code to handle saving more options if needed

        success_message = 'Quiz created successfully!'
        home_url = ''  # Replace with the actual home page URL

        messages.success(request, success_message)
        return redirect('home')

    return render(request, 'create_quiz.html')
from django.shortcuts import render, redirect
from .models import Quiz, Question, Option

from django.shortcuts import render
from .models import Quiz, Question, Option

def save_quiz(request):
    if request.method == 'POST':
        quiz_title = request.POST.get('quiz_title')
        question_count = int(request.POST.get('question_count'))

        # Create a new quiz
        quiz = Quiz.objects.create(title=quiz_title)

        # Save each question and its options
        for i in range(1, question_count + 1):
            question_text = request.POST.get(f'question_{i}')
            correct_answer = request.POST.get(f'correct_answer_{i}')

            question = Question.objects.create(quiz=quiz, text=question_text)

            option1 = Option.objects.create(question=question, text=request.POST.get(f'option_{i}_1'))
            option2 = Option.objects.create(question=question, text=request.POST.get(f'option_{i}_2'))

            # Set the correct answer
            if correct_answer == '1':
                question.correct_option = option1
            elif correct_answer == '2':
                question.correct_option = option2

            question.save()

        return render(request, 'quiz_saved.html')
from django.shortcuts import render
from .models import Quiz

def check_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        quiz_exists = True
    except Quiz.DoesNotExist:
        quiz_exists = False

    context = {
        'quiz_exists': quiz_exists
    }
    return render(request, 'check_quiz.html', context)

def browse_quizzes(request):
    quizzes = Quiz.objects.all()
    context = {
        'quizzes': quizzes
    }
    return render(request, 'browse_quizzes.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Quiz
def view_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Pass the quiz object to the template for rendering
    context = {'quiz': quiz}
    return render(request, 'view_quiz.html', context)



from .models import Quiz, Question, Option
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = quiz.questions.all()
    total_questions = questions.count()
    context = {
        'quiz': quiz,
        'questions': questions,
        'total_questions': total_questions
    }
    return render(request, 'take_quiz.html', context)

def submit_answer(request):
    if request.method == 'POST':
        answer_id = request.POST.get('answer')
        question_number = request.session.get('question_number', 0)
        quiz_id = request.session.get('quiz_id')

        if answer_id:
            # Save the answer or perform any necessary processing
            # based on the selected answer

            # Example: Retrieve the question and selected option
            question = Question.objects.get(id=question_number)
            selected_option = Option.objects.get(id=answer_id)

            # Example: Save the selected option as the answer
            question.answer = selected_option
            question.save()

        if quiz_id is not None:
            quiz = Quiz.objects.get(id=quiz_id)
            questions = quiz.questions.all()
            if question_number < questions.count():
                return redirect('take_quiz', quiz_id=quiz_id)
            else:
                return redirect('submission_result', quiz_id=quiz_id)
    
    return redirect('home')  # Redirect to a suitable page if quiz_id is not available

def submission_result(request, quiz_id):
    # Perform any necessary processing to determine the submission result
    # Example: Retrieve the Quiz object and calculate the score

    quiz = Quiz.objects.get(id=quiz_id)
    # Calculate the score based on the answers
    score = calculate_score(quiz)  # Replace with your own score calculation logic
    
    # Render the template with the score and quiz details
    return render(request, 'submission_result.html', {'quiz': quiz, 'score': score})

def calculate_score(quiz):
    total_questions = quiz.questions.count()
    correct_answers = 0
    
    for question in quiz.questions.all():
        if question.answer and question.answer.is_correct:
            correct_answers += 1
    
    score = (correct_answers / total_questions) * 100
    return score


from .models import SubmissionAnswer  # Import the SubmissionAnswer model

from django.shortcuts import render, get_object_or_404
from .models import Quiz, Option

def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    total_questions = questions.count()
    score = 0

    for question in questions:
        selected_option_id = request.GET.get(f"question_{question.id}")
        if selected_option_id:
            selected_option = get_object_or_404(Option, id=selected_option_id)
            if selected_option.is_correct:
                score += 1

    context = {
        'quiz': quiz,
        'total_questions': total_questions,
        'score': score,
    }

    return render(request, 'quiz_result.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Option, Submission, SubmissionAnswer
from django.urls import reverse
def quiz_submission(request, quiz_id):
    if request.method == 'POST':
        quiz = Quiz.objects.get(pk=quiz_id)
        questions = quiz.questions.all()
        total_questions = questions.count()
        score = 0

        for question in questions:
            selected_option_id = request.POST.get('question_{}'.format(question.id))
            
            # Retrieve the correct option for the question
            correct_option = question.options.get(is_correct=True)
            correct_option_id = correct_option.id

            if selected_option_id == str(correct_option_id):
                score += 1

        context = {
            'quiz': quiz,
            'total_questions': total_questions,
            'score': score
        }
        return render(request, 'quiz_result.html', context)

    return redirect(reverse('browse_quizzes'))