# core/permissions.py
from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class IsAdmin(permissions.BasePermission):
    """Allow only admins (role name 'Admin' or is_staff)."""
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "is_staff", False):
            return True
        role = getattr(user, "role", None)
        return bool(role and role.name and role.name.strip().upper() == "ADMIN")

class IsManager(permissions.BasePermission):
    """Allow managers or admins."""
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "is_staff", False):
            return True
        role = getattr(user, "role", None)
        return bool(role and role.name and role.name.strip().upper() == "MANAGER")

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows object read for all authenticated; write only for owner (creator/owner/user)
    Admins (is_staff) bypass.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "is_staff", False):
            return True
        for attr in ("creator", "owner", "user"):
            if hasattr(obj, attr):
                return getattr(obj, attr) == user
        return False

class IsTaskOwnerOrAssigneeOrAdmin(permissions.BasePermission):
    """
    Allow if user is:
      - admin
      - task.creator
      - assigned to task (via assignments)
    """
    def has_object_permission(self, request, view, obj):
        # Safe methods allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "is_staff", False):
            return True
        if getattr(user, "role", None) and user.role.name.strip().upper() == "ADMIN":
            return True
        # Check creator
        if getattr(obj, "creator", None) == user:
            return True
        # check assignment relation (assumes related_name 'assignments')
        try:
            return obj.assignments.filter(user=user).exists()
        except Exception:
            return False

class IsEditableIfNotCompleted(permissions.BasePermission):
    """
    Deny edits for completed Task objects to non-admins.
    View-level logic should allow status changes if intended.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if getattr(user, "is_staff", False):
            return True
        status = getattr(obj, "status", None)
        completed_flag = None
        # compare to common constant if present
        completed_flag = getattr(obj, "STATUS_COMPLETED", None) or "COMPLETED"
        if status == completed_flag:
            # disallow any write operations (except via explicit complete/uncomplete action handled in view)
            return False
        return True

class HasRolePermission(permissions.BasePermission):
    """
    Check Role -> Permission mapping.
    Views should define attribute `required_permission = "permission.code"`.
    If none set, permission passes by default.
    """
    def has_permission(self, request, view):
        required = getattr(view, "required_permission", None)
        if not required:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "is_staff", False):
            return True
        role = getattr(user, "role", None)
        if not role:
            return False
        # role.role_permissions -> RolePermission objects; query permission.code
        return role.role_permissions.filter(permission__code__iexact=required).exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
