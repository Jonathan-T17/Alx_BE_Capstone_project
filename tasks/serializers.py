# tasks/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import Task, TaskAssignment, Comment
from projects.serializers import ProjectSerializer
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskListSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="username", read_only=True)
    project = serializers.SlugRelatedField(slug_field="name", read_only=True)
    assignees = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ["id", "title", "description", "priority", "status", "due_date", "project", "creator", "assignees", "completed_at"]

    def get_assignees(self, obj):
        users = User.objects.filter(task_assignments__task=obj)
        return [{"id": u.id, "username": u.username, "email": u.email} for u in users]

class TaskDetailSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field="username", read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=ProjectSerializer.Meta.model.objects.all(), required=False, allow_null=True)
    assignees = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    assigned_users = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = ["id", "title", "description", "priority", "status", "due_date", "project", "creator", "assignees", "assigned_users", "completed_at", "created_at", "updated_at"]
        read_only_fields = ["id", "creator", "completed_at", "created_at", "updated_at"]

    def validate_due_date(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def validate(self, attrs):
        # if status is completed then due_date check already done; but check business rule: completed tasks cannot be edited (enforced in update)
        return attrs

    def create(self, validated_data):
        assignees = validated_data.pop("assignees", [])
        request = self.context.get("request")
        if request and not validated_data.get("creator"):
            validated_data["creator"] = request.user
        task = super().create(validated_data)
        # create assignments
        for user_id in assignees:
            try:
                u = User.objects.get(id=user_id)
                TaskAssignment.objects.create(task=task, user=u, assigned_by=request.user if request else None)
            except User.DoesNotExist:
                continue
        return task

    def update(self, instance, validated_data):
        # Prevent editing when completed unless status is changed to non-completed
        if instance.status == Task.STATUS_COMPLETED:
            # allow status change back to non-completed only
            requested_status = validated_data.get("status", instance.status)
            if requested_status == Task.STATUS_COMPLETED:
                # updating while completed but not changing status: forbid (unless admin handles)
                # We'll let permission checks be enforced elsewhere; still prevent accidental edits:
                editable_fields = {"status"}
                for k in list(validated_data.keys()):
                    if k not in editable_fields:
                        raise serializers.ValidationError({"detail": "Completed tasks are read-only. Revert status to edit."})
        assignees = validated_data.pop("assignees", None)
        task = super().update(instance, validated_data)
        # manage assignments if assignees list provided
        request = self.context.get("request")
        if assignees is not None:
            # Replace assignments: simple approach: delete existing then create new
            TaskAssignment.objects.filter(task=task).delete()
            for uid in assignees:
                try:
                    u = User.objects.get(id=uid)
                    TaskAssignment.objects.create(task=task, user=u, assigned_by=request.user if request else None)
                except User.DoesNotExist:
                    continue
        return task

    def get_assigned_users(self, obj):
        users = User.objects.filter(task_assignments__task=obj)
        return [{"id": u.id, "username": u.username, "email": u.email} for u in users]

class TaskAssignmentSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    assigned_by = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = TaskAssignment
        fields = ["id", "task", "user", "assigned_by", "assigned_at"]
        read_only_fields = ["id", "assigned_by", "assigned_at"]

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "task", "user", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request:
            validated_data["user"] = request.user
        return super().create(validated_data)
