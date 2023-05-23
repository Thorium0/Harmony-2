from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import authentication, permissions
from django.contrib.auth.models import User, Group

from channel.views import CreateOrUpdateGroup

from .models import FriendRequest
from .serializers import FriendRequestSerializer



class FriendRequests(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        requests = FriendRequest.objects.filter(toUser=request.user.id, status="P")
 
        data = []

        for friend_request in requests:
            dict = {}
            dict["id"] = friend_request.id
            dict["username"] = friend_request.fromUser.username
            data.append(dict)

        #serializer = FriendRequestSerializer(requests, many=True)

        return Response(data, status=201)
    

    def post(self, request, format=None):
     
        toUser = User.objects.filter(username=request.data["username"])
        if  toUser.exists():
            swapUsers = False
            toUser = toUser.first().id
            fromUser = request.user.id
            if toUser == fromUser:
                return Response({"error": "You cannot send a friend request to yourself"}, status=400)
            data = {
                "fromUser": fromUser,
                "toUser": toUser,
            }
            serializer = FriendRequestSerializer(data=data)
            if serializer.is_valid():
                friendRequest = FriendRequest.objects.filter(fromUser=fromUser, toUser=toUser)
                if not friendRequest.exists():
                    friendRequest = FriendRequest.objects.filter(fromUser=toUser, toUser=fromUser)
                    if friendRequest.exists():
                        swapUsers = True
                if friendRequest.exists():
                    friendRequest = friendRequest.first()
                    if friendRequest.status == "P":
                        return Response({"error": "You have already sent/recieved a friend request to/from this user."}, status=400)
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

        return Response({"error": "A user with that username does not exist"}, status=400)
    

class FriendApprover(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        friendRequest = FriendRequest.objects.filter(id=request.data["id"])
        if not friendRequest.exists():
            return Response({"error": "Friend request does not exist"}, status=400)
        else:
            friendRequest = friendRequest.first()
            if friendRequest.status == "P":
                if request.data["status"] == "A":
                    friendRequest.status = "A"
                    
                    #CreateOrUpdateGroup(friendRequest)
                elif request.data["status"] == "R":
                    friendRequest.status = "R"
                else: 
                    return Response({"error": "Invalid status"}, status=400)
                friendRequest.save()
                return Response(request.data, status=201)
            elif friendRequest.status == "A":
                return Response({"error": "You are already friends with this user"}, status=400)
            else:
                return Response({"error": "Friend request already rejected"}, status=400)
            
        