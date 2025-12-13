# activity/utils.py
from .models import ActivityLog

def log_activity(user, action_type, description="", task=None, project=None):
    """
    Create an ActivityLog entry.
    Keep calls lightweight; do not raise on failure.
    """
    try:
        ActivityLog.objects.create(
            user=user,
            action_type=action_type,
            description=description or "",
            task=task,
            project=project,
        )
    except Exception:
        # swallow to avoid breaking main flow; in prod use logging/error tracking
        pass
