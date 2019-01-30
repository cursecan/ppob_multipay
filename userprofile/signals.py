from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


from .models import (
    Profile, Wallet
)


@receiver(post_save, sender=User)
def initial_user_create(sender, instance, created, **kwargs):
    if created:
        # Create profile
        profile_obj = Profile.objects.create(
            user = instance,
        )
        profile_obj.leader = profile_obj
        profile_obj.save()
        

        # Wallet create
        Wallet.objects.create(
            user = instance,
            profile = profile_obj
        )