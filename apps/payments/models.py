
import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from apps.projects.models import Project
from apps.companies.models import Company
from apps.teams.models import Team
from apps.students.models import Student

class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        SUCCEEDED = "SUCCEEDED", "Réussi"
        FAILED = "FAILED", "Échoué"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="payments")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="payments")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    currency = models.CharField(max_length=10, default="eur")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    stripe_session_id = models.CharField(max_length=255, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def compute_fees(self):
        self.platform_fee = (self.amount * Decimal("0.15")).quantize(Decimal("0.01"))
        self.net_amount = (self.amount - self.platform_fee).quantize(Decimal("0.01"))

    def __str__(self):
        return f"{self.project.title} - {self.amount} {self.currency.upper()} - {self.status}"

class StudentPayment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        PAID = "PAID", "Payé"

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="student_payments")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.username} <- {self.amount}"
