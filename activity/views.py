# create views here.
# activity/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from core.permissions import IsAdmin

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all().select_related("user","task","project")
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "is_staff", False) or (getattr(user, "role", None) and user.role.name.strip().upper()=="ADMIN"):
            return ActivityLog.objects.all()
        return ActivityLog.objects.filter(user=user)
