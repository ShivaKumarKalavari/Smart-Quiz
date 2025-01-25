from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse,redirect, get_object_or_404
from django.utils import timezone

from .utils import update_leaderboard
from .models import User, Admin, Quiz, Question, Option, Response, UserQuiz, AccessList, TopicPerformance, Leaderboard
from django.db.models import F, Max
from django.contrib import messages
from django.contrib.auth.hashers import check_password

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Judge0 API Configuration

JUDGE0_URL = "https://judge0-ce.p.rapidapi.com/submissions"
JUDGE0_HEADERS = {
    "X-RapidAPI-Key": "XXXXXXXXXXXXXXXXXXXXXXXXXxxx",  # Replace with your Judge0 API key
    "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
    "Content-Type": "application/json"
}

""" Testing  purpose """

# Example Problem Data
problem_data = {
    "question": "Implement a function that adds two numbers.",
    "constraints": "1 <= a, b <= 1000",
    "public_test_cases": [
        "Input: a = 2, b = 3 | Output: 5",
        "Input: a = -1, b = 1 | Output: 0"
    ]
}

# Create your views here.
"""
def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})
"""

@login_required
def user_menu(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    print(f"user name: {user.username} user email: {user.email}")
    quizzes = Quiz.objects.filter(title__in= [access_list.quiz for access_list in AccessList.objects.filter(email=user.email)]).order_by('-created_at')
    quiz_list = []
    curr_datetime = timezone.now()
    print(f"Quizes: {quizzes}")
    print(f"Current Time: {curr_datetime}")
    for quiz in quizzes:
        print(f"Quiz: {quiz.title}, Start: {quiz.access_start_time}, End: {quiz.access_end_time}")
        if curr_datetime < quiz.access_end_time and curr_datetime>= quiz.access_start_time:
            quiz_list.append(quiz)
    return render(request,"userMenu.html",{'quizzes':quiz_list, 'user': user})

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    current_time = timezone.now()

    # Ensure the quiz is active and within the access period
    if current_time < quiz.access_start_time or current_time > quiz.access_end_time:
        messages.error(request, 'This quiz is not currently accessible.')
        return redirect('userMenu')

    # Check quiz duration
    time_remaining = (quiz.access_end_time - current_time).total_seconds() / 60
    if time_remaining < quiz.duration:
        quiz.duration = int(time_remaining)  # Adjust duration to remaining time

    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'takeQuiz.html', {'quiz': quiz, 'questions': questions, 'time_remaining': quiz.duration})

def results_view(request):
    score = request.GET.get('score',0)
    total = request.GET.get('total',0)
    attempted = request.GET.get('attempted',0)

    return render(request, 'results.html', {
        'score': score,
        'total': total,
        'attempted': attempted,
    })

def admin_menu(request):
    return render(request,"adminMenu.html")

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Fetch username from form
        password = request.POST.get('password')  # Fetch password from form

        # Check if the user exists
        try:
            user = User.objects.get(username=username)

            # Check password
            if  password == user.password :             # if check_password(password, user.password):
                if user.is_active:
                    # Store user ID in session
                    request.session['user_id'] = user.id
                    try:
                        # Check if the user is an Admin
                        admin = Admin.objects.get(user=user)
                        return redirect('adminMenu')  # Redirect to admin dashboard if admin
                    except Admin.DoesNotExist:
                        # Regular user
                        return redirect('userMenu')  # Redirect to user dashboard
                else:
                    messages.error(request, 'Account is inactive.')
            else:
                messages.error(request, 'Invalid password. Please try again.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username. Please try again.')

    return render(request, 'login.html')


def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        user = get_object_or_404(User, id=request.session.get('user_id'))  # Fetch user from session


        # Create a UserQuiz object to store the user's quiz attempt
        user_quiz = UserQuiz.objects.create(user=user, quiz=quiz)

        score = 0
        total_questions = quiz.questions.count()
        topic_scores = {}

        # Process each question's response
        for question in quiz.questions.all():
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)
                is_correct = selected_option.is_correct

                # Save the user's response
                Response.objects.create(
                    user_quiz=user_quiz,
                    question=question,
                    option=selected_option,
                    is_correct=is_correct,
                    topic=question.topic
                )
                if question.topic not in topic_scores:
                    topic_scores[question.topic] = {'correct': 0, 'total': 0}
                    topic_scores[question.topic]['total'] += 1
                # Update score if the answer is correct
                if is_correct:
                    score += 1
                    topic_scores[question.topic]['correct'] = topic_scores.get(question.topic)['correct'] + 1

        # Save the score and end time
        user_quiz.score = score
        max_attempt = UserQuiz.objects.filter(user=user, quiz=quiz).aggregate(Max('attempt_number'))['attempt_number__max']
        user_quiz.attempt_number = max_attempt + 1
        user_quiz.topicsAndScores = {topic: f"{data['correct']}/{data['total']}" for topic, data in topic_scores.items()}
        user_quiz.end_time = timezone.now()
        user_quiz.save()

        for topic, data in topic_scores.items():
            tp, created = TopicPerformance.objects.get_or_create(user=user, topic=topic)
            tp.questions_attempted += data['total']
            tp.total_score += data['correct']
            tp.save()

        messages.success(request, f'You completed the quiz! Your score is {score}/{total_questions}.')
        return redirect('userMenu')

    return redirect('userMenu')

def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('login')


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def trigger_leaderboard_update(request, quiz_id):
    if request.method == 'POST':  # Allow POST requests for security
        quiz = get_object_or_404(Quiz, id=quiz_id)
        update_leaderboard(quiz)
        messages.success(request, f"Leaderboard updated for quiz: {quiz.title}")
        return redirect('adminMenu')  # Redirect to an appropriate admin page


@csrf_exempt
def execute_code(request):
    if request.method == "POST":
        data = json.loads(request.body)
        payload = {
            "source_code": data["source_code"],  # Map this from frontend
            "language_id": data["language_id"],  # Map this from frontend
            "stdin": data.get("stdin", ""),
        }
        response = requests.post(JUDGE0_URL, headers=JUDGE0_HEADERS, json=payload)
        if response.status_code == 201:
            token = response.json()["token"]
            # Fetch the results using the token
            result = requests.get(f"{JUDGE0_URL}/{token}", headers=JUDGE0_HEADERS)
            return JsonResponse(result.json())
        return JsonResponse({"error": "Failed to create submission"}, status=400)
    # return JsonResponse({"error": "Invalid request"}, status=400)
    return render(request, 'code_execution.html', {'problem': problem_data})





