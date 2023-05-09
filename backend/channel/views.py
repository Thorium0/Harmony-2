from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ChannelSerializer
from .models import Channel


class LatestChannelsList(APIView):
    def get(self, request, format=None):
        channels = Channel.objects.all()[:4]
        serializer = ChannelSerializer(channels, many=True)

        return Response(serializer.data)


