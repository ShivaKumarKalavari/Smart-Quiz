from django.db.models import Max, F
from .models import Quiz, UserQuiz, Leaderboard, User

def update_leaderboard(quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)

    # Skip if ranks are already calculated
    if Leaderboard.objects.filter(quiz=quiz, rank__gt=0).exists():
        return

    # Fetch all UserQuiz records for the quiz, excluding admins
    user_quizzes = (
        UserQuiz.objects.filter(quiz=quiz, user__admin__isnull=True)
        .values('user_id')
        .annotate(max_score=Max('score'))
        .order_by('-max_score')
    )

    # Assign ranks based on descending score
    rank = 1
    for entry in user_quizzes:
        user = User.objects.get(id=entry['user_id'])
        max_score = entry['max_score']

        # Update quiz-specific leaderboard
        leaderboard, created = Leaderboard.objects.get_or_create(
            quiz=quiz,
            user=user,
            defaults={'score': max_score, 'rank': rank}
        )
        leaderboard.score = max_score
        leaderboard.rank = rank
        leaderboard.save()

        rank += 1


    # Update global leaderboard (assume 'Global' is a special quiz entry)
    global_quiz, _ = Quiz.objects.get_or_create(title='Global')
    for entry in user_quizzes:
        user = User.objects.get(id=entry['user_id'])
        max_score = entry['max_score']

        # Update global leaderboard only if not already ranked
        global_leaderboard, created = Leaderboard.objects.get_or_create(
            quiz=global_quiz,
            user=user,
            defaults={'score': 0, 'rank': 0}
        )

        global_leaderboard.score += max_score
        global_leaderboard.save()
        
    leaderboard_users = Leaderboard.objects.filter(quiz=global_quiz, user__admin__isnull=True).order_by('-score')
    rank = 1
    for member in leaderboard_users:
        member.rank = rank
        rank += 1
        member.save() 
    
    user.total_score = F('total_score') + max_score
    user.save()
