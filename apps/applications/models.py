
import uuid
from django.db import models
from django.utils import timezone
from apps.projects.models import Project
from apps.teams.models import Team

class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        ACCEPTED = "ACCEPTED", "Acceptée"
        REJECTED = "REJECTED", "Refusée"
        WITHDRAWN = "WITHDRAWN", "Retirée"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="applications")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)
    proposed_duration = models.PositiveIntegerField(help_text="Durée en jours")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("project", "team")
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.team} -> {self.project} ({self.status})"
