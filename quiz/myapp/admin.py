from django.contrib import admin
from .models import User, Admin, Quiz, Question, Option, UserQuiz, Response, TopicPerformance, Leaderboard, AccessList

admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(UserQuiz)
admin.site.register(Response)
admin.site.register(TopicPerformance)
admin.site.register(Leaderboard)
admin.site.register(AccessList)
