from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def send_user_confirm_code(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


