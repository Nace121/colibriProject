from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User
from .models import Student

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == User.Types.STUDENT:
        Student.objects.get_or_create(user=instance)