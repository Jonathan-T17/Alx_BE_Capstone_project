# projects/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer
from core.permissions import IsOwnerOrReadOnly
from activity.utils import log_activity

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().select_related("owner")
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "is_staff", False) or (getattr(user, "role", None) and user.role.name.strip().upper()=="ADMIN"):
            return Project.objects.all()
        return Project.objects.filter(owner=user)

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        log_activity(self.request.user, "CREATE_PROJECT", f"Created project {project.name}", project=project)
        return project
