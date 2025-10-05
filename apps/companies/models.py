from django.db import models
from django.conf import settings

class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company")
    company_name = models.CharField(max_length=255)
    siret = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name or self.user.username
