
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from apps.students.models import Student

class Team(models.Model):
    class Status(models.TextChoices):
        FORMING = "FORMING", "Forming"
        ACTIVE = "ACTIVE", "Active"
        DISBANDED = "DISBANDED", "Disbanded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    leader = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="led_teams")
    members = models.ManyToManyField(Student, related_name="teams", blank=True)
    specialization = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.FORMING)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.pk:
            if self.members.count() > 4:
                raise ValidationError("Une équipe peut avoir au maximum 4 membres.")
            if self.leader and self.leader not in self.members.all():
                raise ValidationError("Le leader doit être membre de l'équipe.")

    def __str__(self):
        return self.name

class TeamInvitation(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REFUSED = "REFUSED", "Refused"

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="invitations")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="invitations")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    sent_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("team", "student")

    def __str__(self):
        return f"Invitation {self.student} -> {self.team} ({self.status})"
