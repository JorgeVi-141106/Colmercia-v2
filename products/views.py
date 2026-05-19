from rest_framework import viewsets, permissions, filters
from .models import Region, Event, Product
from .serializers import RegionSerializer, EventSerializer, ProductSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.AllowAny]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(activo=True)
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['fecha_inicio', 'fecha_fin']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(activo=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['precio', 'creado_en']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        region = self.request.query_params.get('region')
        categoria = self.request.query_params.get('categoria')
        if region:
            qs = qs.filter(region_id=region)
        if categoria:
            qs = qs.filter(categoria=categoria)
        return qs