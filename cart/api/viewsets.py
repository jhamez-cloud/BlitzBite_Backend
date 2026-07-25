# cart/viewsets.py
from rest_framework.decorators import action
from rest_framework.response import Response
from config.viewsets import StandardViewset
from ..models import Cart, CartItem
from ..serializers import CartSerializer, CartItemSerializer, CartItemWriteSerializer
from ..utils import get_or_create_cart


class CartViewSet(StandardViewset):
    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):
        cart = get_or_create_cart(request)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='apply-coupon')
    def apply_coupon(self, request):
        return Response({"detail": "Coupon logic not yet implemented."}, status=501)


class CartItemViewSet(StandardViewset):

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return CartItemWriteSerializer
        return CartItemSerializer

    def get_queryset(self):
        cart = get_or_create_cart(self.request)
        return CartItem.objects.filter(cart=cart).prefetch_related('cartitemaddon_set__addon')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['cart'] = get_or_create_cart(self.request)
        return context