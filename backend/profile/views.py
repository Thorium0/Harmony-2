from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import ProfileSerializer

def is_alpha(string):
    return all(char.isalpha() for char in string)

class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def put(self, request, format=None):
        data = {}

        try:
            username = request.POST["username"]
        except:
            pass
        else: 
            if not is_alpha(username):
                return Response({"error": "Username can only contain letters in the alphabet"}, status=400)
            if len(username) > 25:
                return Response({"error": "Username is too long"}, status=400)
            data["user"] = {"username": username}

        try:
            data["image"] = request.FILES["image"]
        except:
            pass

        
            


        serializer = ProfileSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.update(request, data)

            try: data["password"] = request.POST["password"]
            except: pass
            else:
                try:
                    request.user.set_password(data["password"])
                    request.user.save()
                except: 
                    return Response({"error": "Failed to set password"}, status=400)

            return Response({"success": "user information updated"}, status=201)
        else:
            return Response({"error": "A user already has this username"}, status=400)