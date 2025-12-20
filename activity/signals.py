# activity/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task
from .models import ActivityLog

@receiver(post_save, sender=Task)
def log_task_activity(sender, instance, created, **kwargs):
    if created:
        action_type = "CREATE_TASK"
        description = f"Task '{instance.title}' was created"
    else:
        action_type = "UPDATE_TASK"
        description = f"Task '{instance.title}' was updated"

    ActivityLog.objects.create(
        user=instance.creator,
        action_type=action_type,
        description=description,
        task=instance
    )
