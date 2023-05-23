from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from channel.views import CreateOrUpdateGroup

from .models import FriendRequest

@receiver(post_save, sender=FriendRequest)
def createProfile(sender, instance, created, **kwargs):
    if created:
        print(instance.toUser)
        #CreateOrUpdateGroup(sender, instance.toUser)


@receiver(post_save, sender=FriendRequest)
def saveProfile(sender, instance, **kwargs):
    print("asdasdasdsadadadsadada")
    #CreateOrUpdateGroup
