from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import ProfileSerializer


class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def put(self, request, format=None):
        data = {}

        try:
            data["user"] = {"username": request.POST["username"]}
        except:
            pass

        try:
            data["image"] = request.FILES["image"]
        except:
            pass
            


        serializer = ProfileSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.update(request, data)
            return Response(serializer.data, status=201)
        else:
            return Response({"error": "A user already has this username"}, status=400)