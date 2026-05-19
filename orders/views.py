from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, CreateOrderSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(comprador=self.request.user)

    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(comprador=request.user)
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart, _ = Cart.objects.get_or_create(comprador=request.user)
        producto_id = request.data.get('producto_id')
        cantidad = int(request.data.get('cantidad', 1))

        from products.models import Product
        producto = Product.objects.get(id=producto_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            producto=producto,
            defaults={'cantidad': cantidad}
        )
        if not created:
            item.cantidad += cantidad
            item.save()

        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='remove_item/(?P<item_id>[^/.]+)')
    def remove_item(self, request, item_id=None):
        CartItem.objects.filter(cart__comprador=request.user, id=item_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(comprador=self.request.user)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            cart = Cart.objects.filter(comprador=request.user).first()
            if not cart or not cart.items.exists():
                return Response({'error': 'Carrito vacío'}, status=status.HTTP_400_BAD_REQUEST)

            total = 0
            order = Order.objects.create(comprador=request.user, total=0)

            for item in cart.items.all():
                subtotal = item.producto.precio * item.cantidad
                total += subtotal
                OrderItem.objects.create(
                    order=order,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.producto.precio
                )

            order.total = total
            order.save()
            cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)