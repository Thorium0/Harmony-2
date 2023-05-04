from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            "category",
            "name",
            "slug",
            "price",
            "date_added",
            "get_absolute_url",
            "get_image",
            "get_thumbnail"
        )