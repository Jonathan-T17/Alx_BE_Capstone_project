# teams/serializers.py
from rest_framework import serializers
from .models import Team, TeamMember
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamMemberSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    class Meta:
        model = TeamMember
        fields = ["id", "team", "user", "joined_at"]
        read_only_fields = ["id", "joined_at"]

class TeamSerializer(serializers.ModelSerializer):
    manager = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), allow_null=True, required=False)
    members = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ["id", "name", "manager", "members", "created_at"]
        read_only_fields = ["id", "members", "created_at"]

    def get_members(self, obj):
        users = User.objects.filter(team_memberships__team=obj)
        return [{"id": u.id, "username": u.username, "email": u.email} for u in users]

    def create(self, validated_data):
        return super().create(validated_data)
