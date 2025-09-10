from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# whats happening in signals is that when a new CustomUser is created, a corresponding UserProfile is automatically created and linked to that user. This ensures that every user has an associated profile without requiring manual creation of the profile after the user is created.