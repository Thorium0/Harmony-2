from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import authentication, permissions

from .models import FriendRequest
from .serializers import FriendRequestSerializer


class FriendRequests(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        requests = FriendRequest.objects.filter(toUser=request.user.id)
 
        data = []

        for friend_request in requests:
            dict = {}
            dict["id"] = friend_request.id
            dict["username"] = friend_request.fromUser.username
            data.append(dict)

        #serializer = FriendRequestSerializer(requests, many=True)

        return Response(data)
    

    def post(self, request, format=None):
        serializer = FriendRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            swapUsers = False
            friendRequest = FriendRequest.objects.filter(fromUser=serializer.validated_data["fromUser"], toUser=serializer.validated_data["toUser"])
            if not friendRequest.exists():
                friendRequest = FriendRequest.objects.filter(fromUser=serializer.validated_data["toUser"], toUser=serializer.validated_data["fromUser"])
                if friendRequest.exists():
                    swapUsers = True
            if friendRequest.exists():
                friendRequest = friendRequest.first()
                if friendRequest.status == "P":
                    return Response({"error": "You already have sent/recieved a friend request to/from this user."}, status=400)
                elif friendRequest.status == "A":
                    return Response({"error": "You are already friends with this user"}, status=400)
                else:
                    friendRequest.status = "P"
                    if swapUsers:
                        tempUser = friendRequest.fromUser
                        friendRequest.fromUser = friendRequest.toUser
                        friendRequest.toUser = tempUser
                    friendRequest.save()
                    return Response(serializer.data, status=201)
            

            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)