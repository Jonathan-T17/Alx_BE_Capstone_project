# Register models here.
# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Profile, PasswordResetToken

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ("username", "email", "is_active", "role")
    search_fields = ("username", "email")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "job_title", "department")

@admin.register(PasswordResetToken)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "expires_at", "is_used")
    readonly_fields = ("id",)
