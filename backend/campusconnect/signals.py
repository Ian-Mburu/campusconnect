from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import StudentProfile, TeacherProfile, AdminProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "student":
            StudentProfile.objects.create(user=instance)
        elif instance.user_type == "lecturer":
            TeacherProfile.objects.create(user=instance)
        elif instance.user_type == "admin":
            AdminProfile.objects.create(user=instance)
