# Generated by Django 5.1.2 on 2025-01-01 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_leaderboard_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquiz',
            name='attempt_number',
            field=models.IntegerField(default=0),
        ),
    ]
