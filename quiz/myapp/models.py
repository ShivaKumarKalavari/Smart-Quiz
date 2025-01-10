from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    college = models.CharField(max_length=255,default='Unknown')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    total_score = models.FloatField(default=0.0)  # New field for overall leaderboard

    def __str__(self):
        return self.username


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensures each admin is linked to one user
    role = models.CharField(max_length=50)
    permissions = models.JSONField()  # Assuming JSON field to store permissions

    def __str__(self):
        return f'{self.user.username} - {self.role}'


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    quiz_type = models.CharField(max_length=50, choices=[('multiple_choice', 'Multiple Choice'), ('coding', 'Coding')], default='multiple_choice')
    created_by = models.ForeignKey(Admin, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    access_start_time = models.DateTimeField()  # Access period start time
    access_end_time = models.DateTimeField()  # Access period end time
    duration = models.IntegerField(default=30)  # Duration in minutes

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=50, choices=[('multiple_choice', 'Multiple Choice')])
    topic = models.CharField(max_length=100,default='others')  # New field to categorize questions by topic
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]  # Display first 50 chars


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


class UserQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    attempt_number = models.IntegerField(default=0)  # Tracks attempt numbers
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    topicsAndScores = models.JSONField(default=dict)  # storing like this {'English': '45/50', ...}

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title} (Attempt {self.attempt_number})'


class Response(models.Model):
    user_quiz = models.ForeignKey(UserQuiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    topic = models.CharField(max_length=100, default='others')

    def __str__(self):
        return f'{self.user_quiz.user.username} - {self.question.text[:50]}'


class TopicPerformance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)  # Topic name
    questions_attempted = models.IntegerField(default=0)  # Number of quizzes attempted for this topic
    total_score = models.FloatField(default=0.0)  # Total score in this topic

    def __str__(self):
        return f'{self.user.username} - {self.topic}'


class Leaderboard(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)  # Specific quiz or overall
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    rank = models.IntegerField(default=0)  # Rank of the user for this quiz or overall

    def __str__(self):
        if self.quiz:
            return f'{self.user.username} - {self.quiz.title} - Rank {self.rank}'
        else:
            return f'{self.user.username} - Overall - Rank {self.rank}'
        
class AccessList(models.Model):
    email = models.EmailField()  # User email
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)  # Quiz the user has access to

    class Meta:
        unique_together = ['email', 'quiz']

    def __str__(self):
        return f'{self.email} - {self.quiz.title}'
    
class Problem(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='problems')  # Relationship with Quiz
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=100,default='coding')
    description = models.TextField()
    constraints = models.TextField()
    public_test_cases = models.JSONField(default=list)  # Store public test cases as a JSON array
    hidden_test_cases = models.JSONField(default=list)  # Store hidden test cases as a JSON array (for evaluation purposes)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Quiz: {self.quiz.title})"
