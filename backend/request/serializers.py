from rest_framework import serializers
from .models import FriendRequest
from django.contrib.auth.models import User


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = (
            "id",
            "fromUser",
            "toUser",
            "status",
            "created",
            "updated",
        )

