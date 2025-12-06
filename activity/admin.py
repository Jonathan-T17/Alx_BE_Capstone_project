# Register models here.
# activity/admin.py
from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("action_type", "user", "timestamp")
    list_filter = ("action_type",)
    search_fields = ("description", "user__username")
