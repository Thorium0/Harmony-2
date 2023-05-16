from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User, Group

"""
 data_group["members"] = []
            users = User.objects.filter(groups__name=group.name)
            for user in users:
                data_group["members"].append(user.username)
"""

class FriendChannels(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        groups = request.user.groups.all()
       
        data = []

        for group in groups:
            data_group = {}
            data_group["name"] = group.name
            friend = User.objects.filter(groups__name=group.name).exclude(id=request.user.id).first()
            data_group["friend"] = {
                "id": friend.id,
                "username": friend.username,
                "image": friend.profile.image.url
            }

           
            data.append(data_group)
        

        return Response(data, status=201)

def CreateOrUpdateGroup(user1, user2):


        if user1 == user2:
            return Response({"error": "You cannot create a channel with yourself"}, status=400)

        group = Group.objects.filter(name=str(user2.id) +"_"+ str(user1.id))
        if group.exists():
            group = group.first()
        else:
            group = Group.objects.get_or_create(name=str(user1.id) +"_"+ str(user2.id))[0]

      
        user1.groups.add(group)
        user2.groups.add(group)

        return Response("Channel created", status=201)

