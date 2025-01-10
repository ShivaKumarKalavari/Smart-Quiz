from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Quiz
from .utils import update_leaderboard
import threading

@receiver(post_save, sender=Quiz)
def schedule_leaderboard_update(sender, instance, **kwargs):
    # Only schedule if access_end_time is in the future
    if instance.access_end_time > now():
        # Calculate the delay in seconds
        delay = (instance.access_end_time - now()).total_seconds() + 60  # Add 1 minute buffer
        threading.Timer(delay, update_leaderboard, args=[instance.id]).start()
