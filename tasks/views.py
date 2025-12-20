# tasks/views.py
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Task
from .filters import TaskFilter
from .permissions import IsTaskOwnerOrAssigneeOrAdmin,IsEditableIfNotCompleted
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task, TaskAssignment, Comment
from .serializers import TaskListSerializer, TaskDetailSerializer, TaskAssignmentSerializer, CommentSerializer
from core.permissions import IsTaskOwnerOrAssigneeOrAdmin, HasRolePermission, IsEditableIfNotCompleted
from activity.utils import log_activity

User = get_user_model()

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all().select_related("creator", "project")
    permission_classes = [IsAuthenticated, IsTaskOwnerOrAssigneeOrAdmin, IsEditableIfNotCompleted]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "priority", "project", "creator"]
    ordering_fields = ["due_date", "priority", "created_at"]
    ordering = ["-created_at"]
    search_fields = ["title", "description", "creator__username", "assignees__username"]

    def get_serializer_class(self):
        if self.action == "list":
            return TaskListSerializer
        return TaskDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "is_staff", False) or (getattr(user, "role", None) and user.role.name.strip().upper() == "ADMIN"):
            return Task.objects.all()
        return Task.objects.filter(models.Q(creator=user) | models.Q(assignments__user=user)).distinct()

    def perform_create(self, serializer):
        task = serializer.save(creator=self.request.user)
        log_activity(self.request.user, "CREATE_TASK", f"Created task {task.title}", task=task)
        return task

    @action(detail=True, methods=["post"], url_path="assign", permission_classes=[IsAuthenticated, HasRolePermission])
    def assign(self, request, pk=None):
        """
        Body: { "assignees": ["uuid1", "uuid2", ...] }
        The view should set required_permission = 'task.assign' before dispatch, or router-level handling.
        """
        # optional: check view attribute for required_permission - but HasRolePermission uses it
        task = self.get_object()
        assignees = request.data.get("assignees", [])
        created = []
        for uid in assignees:
            try:
                user = User.objects.get(id=uid)
            except User.DoesNotExist:
                continue
            ta, created_flag = TaskAssignment.objects.get_or_create(task=task, user=user, defaults={"assigned_by": request.user})
            if created_flag:
                created.append(str(user.username))
                log_activity(request.user, "ASSIGN_USER", f"Assigned {user.username} to {task.title}", task=task)
        return Response({"assigned": created}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="complete", permission_classes=[IsAuthenticated, IsTaskOwnerOrAssigneeOrAdmin])
    def complete(self, request, pk=None):
        """
        Body: { "completed": true/false }
        """
        task = self.get_object()
        completed = request.data.get("completed", True)
        if completed in (True, "true", "True", "1", 1):
            if task.status == Task.STATUS_COMPLETED:
                return Response({"detail": "Task already completed."}, status=status.HTTP_400_BAD_REQUEST)
            task.status = Task.STATUS_COMPLETED
            task.completed_at = timezone.now()
            task.save()
            log_activity(request.user, "COMPLETE_TASK", f"Completed task {task.title}", task=task)
            return Response({"detail": "Task marked completed."}, status=status.HTTP_200_OK)
        else:
            # revert to pending (only creator or admin)
            if not (task.creator == request.user or getattr(request.user, "is_staff", False)):
                return Response({"detail": "Only creator or admin can revert completion."}, status=status.HTTP_403_FORBIDDEN)
            task.status = Task.STATUS_PENDING
            task.completed_at = None
            task.save()
            log_activity(request.user, "UPDATE_TASK", f"Reverted completion for {task.title}", task=task)
            return Response({"detail": "Task reverted to pending."}, status=status.HTTP_200_OK)
