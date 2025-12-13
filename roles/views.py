# roles/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Role, Permission, RolePermission
from .serializers import RoleSerializer, PermissionSerializer, RolePermissionSerializer
from core.permissions import IsAdmin

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
