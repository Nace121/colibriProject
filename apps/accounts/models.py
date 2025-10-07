from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Types(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        COMPANY = "COMPANY", "Company"

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=Types.choices, default=Types.STUDENT)

    def __str__(self):
        return self.username
