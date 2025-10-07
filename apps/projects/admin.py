
from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title","company","category","budget","status","created_at")
    list_filter = ("category","status")
    search_fields = ("title","description","company__company_name")
