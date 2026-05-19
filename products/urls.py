from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegionViewSet, EventViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'regions', RegionViewSet)
router.register(r'events', EventViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]