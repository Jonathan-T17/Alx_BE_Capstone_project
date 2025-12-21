from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        "status": "OK",
        "message": "Task Management API is live!",
        "auth": [
            "Register a new user → /api/auth/register/",
            "Login and get token → /api/auth/token/",
        ],
        "resources": [
            "Users → /api/users/",
            "Projects → /api/projects/",
            "Tasks → /api/tasks/",
            "Teams → /api/teams/",
            "Roles → /api/roles/",
            "Activity → /api/activity/",
        ],
    })
