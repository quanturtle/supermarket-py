from datetime import datetime
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Supermarket, Link, Product
from .serializers import SupermarketSerializer, LinkSerializer, ProductSerializer


class SupermarketViewSet(ModelViewSet):
    queryset = Supermarket.objects.all()
    serializer_class = SupermarketSerializer

    def create(self, request):
        new_supermarket = request.data
        
        supermarket, created = Supermarket.objects.get_or_create(name=new_supermarket['name'])
        
        if created:
            supermarket.base_url = new_supermarket['base_url']
            supermarket.base_url_https = new_supermarket['base_url_https']
            supermarket.domain = new_supermarket['domain']
            supermarket.save()

            serializer = SupermarketSerializer(supermarket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        supermarket.updated_at = datetime.now()
        supermarket.save()

        serializer = SupermarketSerializer(supermarket)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LinkViewSet(ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['supermarket']

    def create(self, request):
        new_link = request.data
        supermarket = get_object_or_404(Supermarket, pk=new_link['supermarket'])

        link, created = Link.objects.get_or_create(
            supermarket=supermarket,
            url=new_link['url'],
        )
        
        if created:
            link.created_at = datetime.now()
            link.updated_at = datetime.now()
            link.save()

            serializer = LinkSerializer(link)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        link.updated_at = datetime.now()
        link.save()

        serializer = LinkSerializer(link)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['supermarket']

    def create(self, request):
        new_product = request.data
        supermarket = get_object_or_404(Supermarket, pk=new_product['supermarket'])

        product, created = Product.objects.get_or_create(
            supermarket=supermarket,
            url=new_product['url'],
            sku=new_product['sku'],
            name=new_product['name'],
            current_price=new_product['current_price']
        )
        
        if created:
            product.created_at = datetime.now()
            product.updated_at = datetime.now()
            product.save()

            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        product.updated_at = datetime.now()
        product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)