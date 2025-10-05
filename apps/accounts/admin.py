from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("username", "email", "user_type", "is_staff", "is_verified")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Profil", {"fields": ("user_type", "is_verified", "phone", "avatar")}),
    )
