
from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("project","team","proposed_price","proposed_duration","status","submitted_at")
    list_filter = ("status",)
    search_fields = ("project__title","team__name")
