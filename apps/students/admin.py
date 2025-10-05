from django.contrib import admin
from .models import Student, Skill

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user","university","level")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ("name",)
