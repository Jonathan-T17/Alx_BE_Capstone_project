# Create models here.
# activity/models.py
import uuid
from django.db import models
from django.conf import settings

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("CREATE_TASK", "Create Task"),
        ("UPDATE_TASK", "Update Task"),
        ("DELETE_TASK", "Delete Task"),
        ("ASSIGN_USER", "Assign User"),
        ("COMPLETE_TASK", "Complete Task"),
        ("PASSWORD_RESET", "Password Reset"),
        ("CREATE_PROJECT", "Create Project"),
        ("CREATE_TEAM", "Create Team"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="activity_logs")
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    task = models.ForeignKey("tasks.Task", on_delete=models.SET_NULL, null=True, blank=True, related_name="activity_logs")
    project = models.ForeignKey("projects.Project", on_delete=models.SET_NULL, null=True, blank=True, related_name="activity_logs")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "action_type"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"{self.action_type} by {self.user} at {self.timestamp}"
