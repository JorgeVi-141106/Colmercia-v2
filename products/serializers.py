from rest_framework import serializers
from .models import Region, Event, Product


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'nombre', 'descripcion', 'historia_cultural', 'imagen', 'creado_en']
        read_only_fields = ['id', 'creado_en']


class EventSerializer(serializers.ModelSerializer):
    region_nombre = serializers.CharField(source='region.nombre', read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'nombre', 'region', 'region_nombre', 'fecha_inicio', 'fecha_fin', 'descripcion', 'activo', 'creado_en']
        read_only_fields = ['id', 'creado_en']


class ProductSerializer(serializers.ModelSerializer):
    vendedor_nombre = serializers.CharField(source='vendedor.get_full_name', read_only=True)
    region_nombre = serializers.CharField(source='region.nombre', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'region', 'region_nombre', 'vendedor', 'vendedor_nombre', 'categoria', 'imagen', 'activo', 'creado_en', 'actualizado_en']
        read_only_fields = ['id', 'creado_en', 'actualizado_en']