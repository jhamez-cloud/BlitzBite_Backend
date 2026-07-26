# orders/viewsets.py
from rest_framework.decorators import action
from rest_framework.response import Response
from config.viewsets import StandardViewset
from cart.utils import get_or_create_cart
from ..models import Order
from ..serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer,
    OrderCancelSerializer,
)
from ..services import create_order_from_cart


class OrderViewSet(StandardViewset):
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Once auth exists, scope this to request.user. For now, unscoped
        # since there's no logged-in user to filter by yet — flagged as TODO.
        return Order.objects.select_related('restaurant').prefetch_related(
            'order_items__addons', 'order_timeline'
        )

    def create(self, request, *args, **kwargs):
        input_serializer = OrderCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        cart = get_or_create_cart(request)

        try:
            order = create_order_from_cart(
                cart=cart,
                user=request.user if request.user.is_authenticated else None,
                delivery_address=data['delivery_address'],
                payment_method=data['payment_method'],
                tip=data.get('tip', 0),
                coupon_code=data.get('coupon_code'),
            )
        except ValueError as e:
            return Response({'detail': str(e)}, status=400)

        return Response(OrderSerializer(order).data, status=201)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        serializer = OrderCancelSerializer(data={}, context={'order': order})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(order).data)