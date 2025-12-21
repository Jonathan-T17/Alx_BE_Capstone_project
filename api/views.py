# api/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        "status": "OK",
        "message": "🎉 Task Management API is live and running",

        "authentication": {
            "register": {
                "message": "Create a new user account",
                "endpoint": "/api/auth/register/",
                "method": "POST"
            },
            "login": {
                "message": "Obtain JWT access and refresh tokens",
                "endpoint": "/api/auth/token/",
                "method": "POST"
            }
        },

        "applications": {
            "users": {
                "message": "Manage system users and profiles (Admin only)",
                "endpoint": "/api/users/",
                "authentication": "Required (JWT)"
            },
            "projects": {
                "message": "Create and manage projects",
                "endpoint": "/api/projects/",
                "authentication": "Required (JWT)"
            },
            "tasks": {
                "message": "Create, assign, and track tasks",
                "endpoint": "/api/tasks/",
                "authentication": "Required (JWT)"
            },
            "teams": {
                "message": "Manage teams and memberships",
                "endpoint": "/api/teams/",
                "authentication": "Required (JWT)"
            },
            "roles": {
                "message": "Define and manage user roles",
                "endpoint": "/api/roles/",
                "authentication": "Admin only"
            },
            "activity": {
                "message": "View system activity logs",
                "endpoint": "/api/activity/",
                "authentication": "Admin only"
            }
        }
    })
