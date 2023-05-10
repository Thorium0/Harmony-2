from django.db import models
from django.contrib.auth.models import User


class FriendRequest(models.Model):

    STATUS_CHOICES = (
        ("P", "pending"),
        ("A", "accepted"),
        ("R", "rejected"),
    )

    fromUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fromUser', null=True)
    toUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='toUser', null=True)
    status = models.CharField(max_length=100, default="P", choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}: {self.fromUser.username} -> {self.toUser.username}'
