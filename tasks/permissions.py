from rest_framework.permissions import BasePermission

class IsTaskOwnerOrAssigneeOrAdmin(BasePermission):
    """
    Only task owner, assigned users, or admin can access
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if obj.owner == request.user:
            return True

        return obj.assignees.filter(id=request.user.id).exists()


class IsEditableIfNotCompleted(BasePermission):
    """
    Prevent editing completed tasks unless reverted
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return not obj.completed
        return True
