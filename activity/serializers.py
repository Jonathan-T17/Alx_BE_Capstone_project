# activity/serializers.py
from rest_framework import serializers
from .models import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    task = serializers.PrimaryKeyRelatedField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ActivityLog
        fields = ["id", "user", "action_type", "description", "task", "project", "timestamp"]
        read_only_fields = ["id", "user", "timestamp"]
