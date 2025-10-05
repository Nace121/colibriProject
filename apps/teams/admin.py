
from django.contrib import admin
from .models import Team, TeamInvitation

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name","leader","status","created_at")
    search_fields = ("name",)

@admin.register(TeamInvitation)
class TeamInvitationAdmin(admin.ModelAdmin):
    list_display = ("team","student","status","sent_at","responded_at")
    list_filter = ("status",)
