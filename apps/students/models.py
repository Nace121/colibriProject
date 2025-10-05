from django.db import models
from django.conf import settings

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    LEVELS = [("L1","L1"),("L2","L2"),("L3","L3"),("M1","M1"),("M2","M2")]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student")
    university = models.CharField(max_length=150, blank=True)
    level = models.CharField(max_length=2, choices=LEVELS, blank=True)
    specialization = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    cv = models.FileField(upload_to="cvs/", blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.user.username
