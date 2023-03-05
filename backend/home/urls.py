from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SupermarketViewSet, LinkViewSet, ProductViewSet

router = DefaultRouter()

router.register('supermarket', SupermarketViewSet, basename="supermarket")
router.register('link', LinkViewSet, basename="link")
router.register('product', ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]