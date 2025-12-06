# Register models here.
# tasks/admin.py
from django.contrib import admin
from .models import Task, TaskAssignment, Comment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "status", "priority", "due_date")
    list_filter = ("status", "priority")
    search_fields = ("title", "creator__username")

@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "assigned_by", "assigned_at")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "created_at")
    search_fields = ("task__title", "user__username", "content")
