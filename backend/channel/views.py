from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ChannelSerializer
from .models import Channel


class LatestChannelsList(APIView):
    def get(self, resquest, format=None):
        channels = Channel.objects.all()[:4]
        serializer = ChannelSerializer(channels, many=True)

        return Response(serializer.data)


"""
class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")


    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
"""