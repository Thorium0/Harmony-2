from django.db.models.signals import pre_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from channel.views import CreateOrUpdateGroup, delGroup

from .models import FriendRequest

@receiver(pre_save, sender=FriendRequest)
def createRequest(sender, instance, **kwargs):
    if instance.status == "A":
        group = CreateOrUpdateGroup(instance)
        instance.group = group


@receiver(pre_save, sender=FriendRequest)
def saveRequest(sender, instance, **kwargs):
    if instance.status == "A":
        group = CreateOrUpdateGroup(instance)
        instance.group = group
    else: 
        delGroup(instance)
        instance.group = None
