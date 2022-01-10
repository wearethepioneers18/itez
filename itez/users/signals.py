from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile, UserWorkDetail


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):


@receiver(post_save, sender=User)
def create_user_work_detail(sender, instance, created, **kwargs):
    if created:
        UserWorkDetail.objects.create(user=instance)
        instance.user_work_detail.save()


# @receiver(post_save, sender=User)
# def save_user_work_detail(sender, instance, **kwargs):
