# projects/serializers.py
from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "owner", "start_date", "end_date", "created_at", "updated_at"]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def create(self, validated_data):
        # owner should be set in view from request.user
        return super().create(validated_data)
