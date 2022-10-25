from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import CommonUserProfile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    """ Create a profile for the verified user if a profile
    already doesn't belong to the user.
    """
    if created:
        try:
            profile = instance.profile
        except CommonUserProfile.DoesNotExist:
            CommonUserProfile.objects.create(user=instance)


'''@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
'''
