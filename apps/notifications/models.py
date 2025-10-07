import uuid
from django.db import models
from django.utils import timezone
from apps.accounts.models import User

class Notification(models.Model):
    class Type(models.TextChoices):
        INFO = "INFO", "Info"
        APPLICATION_SUBMITTED = "APPLICATION_SUBMITTED", "Candidature envoyée"
        APPLICATION_ACCEPTED = "APPLICATION_ACCEPTED", "Candidature acceptée"
        APPLICATION_REJECTED = "APPLICATION_REJECTED", "Candidature refusée"
        TEAM_INVITE = "TEAM_INVITE", "Invitation d'équipe"
        PAYMENT_SUCCEEDED = "PAYMENT_SUCCEEDED", "Paiement confirmé"
        PROJECT_STATUS = "PROJECT_STATUS", "Statut projet"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=40, choices=Type.choices, default=Type.INFO)
    message = models.TextField()
    url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def mark_read(self):
        if not self.is_read:
            self.is_read = True
            from django.utils import timezone
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at"])

    def __str__(self):
        return f"{self.recipient} - {self.type}"
