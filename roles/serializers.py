# roles/serializers.py
from rest_framework import serializers
from .models import Role, Permission, RolePermission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "code", "description"]

class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ["id", "name", "description", "permissions"]

    def get_permissions(self, obj):
        perms = Permission.objects.filter(role_permissions__role=obj).distinct()
        return PermissionSerializer(perms, many=True).data

class RoleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "description"]

class RolePermissionSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(slug_field="name", queryset=Role.objects.all())
    permission = serializers.SlugRelatedField(slug_field="code", queryset=Permission.objects.all())

    class Meta:
        model = RolePermission
        fields = ["id", "role", "permission"]
