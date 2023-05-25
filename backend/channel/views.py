from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User, Group
from datetime import datetime

from request.models import FriendRequest

from .models import Message
from .serializers import MessageSerializer

class FriendChannels(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        groups = request.user.groups.all()
       
        data = []

        for group in groups:
            data_group = {}
            data_group["name"] = group.name
            data_group["id"] = group.id
            friend = User.objects.filter(groups__name=group.name).exclude(id=request.user.id).first()
            data_group["friend"] = {
                "id": friend.id,
                "username": friend.username,
                "image": friend.profile.image.url
            }

           
            data.append(data_group)
        

        return Response(data, status=201)

def CreateOrUpdateGroup(instance):
        user1 = instance.fromUser_id
        user2 = instance.toUser_id

        if user1 == user2:
            return Response({"error": "You cannot create a channel with yourself"}, status=400)

        group = Group.objects.filter(name=str(user2) +"_"+ str(user1))
        if group.exists():
            group = group.first()
        else:
            group = Group.objects.get_or_create(name=str(user1) +"_"+ str(user2))[0]

        user1_instance = User.objects.get(id=user1)
        user1_instance.groups.add(group)

        user2_instance = User.objects.get(id=user2)
        user2_instance.groups.add(group)
        

        return group


def delGroup(instance):
    group = Group.objects.filter(id=instance.group_id)
    group.delete()




class Messages(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


    def get(self, request, channel_id, format=None):
        group = Group.objects.filter(id=channel_id)
        if group.exists():
            group = group.first()
            if not request.user in group.user_set.all():
                return Response({"error": "You are not in this channel"}, status=400)
            messages = Message.objects.filter(group=group).order_by('-created')

            data = []
            for message in messages:
                dict = {}
                dict["id"] = message.id
                dict["content"] = message.content
                time = message.created
                if time.date() == datetime.today().date():
                     dict["created"] = time.strftime("Today at %H:%M:%S")
                else:
                     dict["created"] = time.strftime("%d/%m/%Y %H:%M")
                dict["sender"] = {
                    "id": message.sender.id,
                    "username": message.sender.username,
                    "image": message.sender.profile.image.url
                }
                data.append(dict)
            return Response(data, status=201)
        else:
            return Response({"error": "Channel does not exist"}, status=400)
        


    def post(self, request, channel_id, format=None):
        group = Group.objects.filter(id=channel_id)
        if group.exists():
            group = group.first()
            if not request.user in group.user_set.all():
                return Response({"error": "You are not in this channel"}, status=400)
            data = {
                "group": group.id,
                "content": request.data["content"],
                "sender": request.user.id
            }
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        else:
            return Response({"error": "Channel does not exist"}, status=400)