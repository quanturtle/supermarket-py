from rest_framework.serializers import ModelSerializer 
from .models import Supermarket, Link, Product


class SupermarketSerializer(ModelSerializer):
    class Meta:
        model = Supermarket
        fields = ('id', 'name', 'base_url', 'base_url_https', 'domain')


class LinkSerializer(ModelSerializer):
    class Meta:
        model = Link
        fields = ('id', 'supermarket', 'url', 'created_at', 'updated_at')


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'supermarket', 'url', 'sku', 'name', 'current_price', 'created_at', 'updated_at')