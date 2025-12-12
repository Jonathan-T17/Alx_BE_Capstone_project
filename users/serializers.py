# users/serializers.py
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, PasswordResetToken
from roles.models import Role

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "phone", "job_title", "department", "avatar_url"]

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    role = serializers.SlugRelatedField(slug_field="name", queryset=Role.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_active", "role", "profile"]
        read_only_fields = ["id", "is_active"]

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2", "first_name", "last_name", "role"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2", None)
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # Profile auto-created using signals
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password2 = serializers.CharField(min_length=8)

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        # token validation is normally done in the view; keeping simple here
        return attrs

class PasswordResetTokenSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = PasswordResetToken
        fields = ["id", "user", "token", "expires_at", "is_used"]
        read_only_fields = ["id", "user", "expires_at", "is_used"]
