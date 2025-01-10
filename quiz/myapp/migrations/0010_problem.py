# Generated by Django 5.1.2 on 2025-01-10 05:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_quiz_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('constraints', models.TextField()),
                ('public_test_cases', models.JSONField(default=list)),
                ('hidden_test_cases', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='myapp.quiz')),
            ],
        ),
    ]
