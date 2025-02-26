# Generated by Django 5.1.2 on 2024-12-30 11:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_question_topic_userquiz_attempt_number_leaderboard_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topicperformance',
            old_name='quizzes_attempted',
            new_name='questions_attempted',
        ),
        migrations.RemoveField(
            model_name='topicperformance',
            name='average_score',
        ),
        migrations.AddField(
            model_name='user',
            name='college',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AddField(
            model_name='userquiz',
            name='topicsAndScores',
            field=models.JSONField(default=None),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AccessList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('access_start_time', models.DateTimeField()),
                ('access_end_time', models.DateTimeField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.quiz')),
            ],
        ),
    ]
