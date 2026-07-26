# orders/serializers.py
from django.utils import timezone
from rest_framework import serializers
from .models import Order, OrderItem, OrderItemAddon, OrdersTimeLineEntry


class OrderItemAddonSerializer(serializers.ModelSerializer):
    """Read-only — addons are snapshotted at order-creation time,
    never edited after the fact."""
    class Meta:
        model = OrderItemAddon
        fields = ['id', 'name', 'price', 'quantity']
        read_only_fields = fields  # everything here is historical, nothing writable


class OrderItemSerializer(serializers.ModelSerializer):
    """Read-only — order items are created once, atomically, as part of
    order creation (see create_order_from_cart). No direct write endpoint."""
    addons = OrderItemAddonSerializer(many=True, read_only=True)
    menu_item_id = serializers.IntegerField(source='menu_item.id', read_only=True, allow_null=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item_id', 'name', 'price', 'quantity', 'subtotal', 'addons']
        read_only_fields = fields


class OrdersTimeLineEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersTimeLineEntry
        fields = ['id', 'status', 'label', 'time', 'completed']
        read_only_fields = ['id']
        # Note: writable for now since staff/admin will need to update timeline
        # entries as an order progresses — will be locked to staff-only permissions
        # once auth exists.


class OrderSerializer(serializers.ModelSerializer):
    """Read-side — full order detail, matches your original spec's response shape."""
    items = OrderItemSerializer(many=True, read_only=True)
    timeline = OrdersTimeLineEntrySerializer(source='order_timeline', many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    restaurant_id = serializers.IntegerField(source='restaurant.id', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'restaurant_id', 'items', 'subtotal',
            'delivery_fee', 'discount', 'tip', 'total', 'status',
            'estimated_delivery_time', 'delivery_address', 'payment_method',
            'courier', 'timeline', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'order_id', 'restaurant_id', 'items', 'subtotal', 'total',
            'status', 'estimated_delivery_time', 'courier', 'timeline',
            'created_at', 'updated_at',
        ]
        # Note: 'items' comes from related_name='order_items' on OrderItem,
        # but DRF resolves it via the model's related_name automatically —
        # since it matches the field name here, no source= needed.


class OrderCreateSerializer(serializers.Serializer):
    """Not a ModelSerializer — an order is built from the current cart via
    a service function, not a direct field-by-field model write. This just
    validates the handful of things the client actually supplies at checkout."""
    delivery_address = serializers.CharField()
    payment_method = serializers.CharField()
    coupon_code = serializers.CharField(required=False, allow_blank=True)
    tip = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)

    def validate_tip(self, value):
        if value < 0:
            raise serializers.ValidationError("tip cannot be negative.")
        return value


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Staff-only status transitions — PATCH /orders/{id}/status/"""
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        current = self.instance.status if self.instance else None
        terminal_statuses = {Order.OrderStatus.DELIVERED, Order.OrderStatus.CANCELLED}

        if current in terminal_statuses and value != current:
            raise serializers.ValidationError(
                f"Cannot change status of an order that is already '{current}'."
            )

        if value == Order.OrderStatus.CANCELLED and current != Order.OrderStatus.PENDING:
            raise serializers.ValidationError(
                "Orders can only be cancelled while still 'pending'. "
                f"This order is already '{current}'."
            )

        return value
    
class OrderCancelSerializer(serializers.Serializer):
    """Used by POST /orders/{id}/cancel/ — no input fields needed,
    just validates that the order is still cancellable."""

    def validate(self, attrs):
        order = self.context['order']
        if order.status != Order.OrderStatus.PENDING:
            raise serializers.ValidationError(
                f"This order can no longer be cancelled — its status is '{order.status}'."
            )
        return attrs

    def save(self):
        order = self.context['order']
        order.status = Order.OrderStatus.CANCELLED
        order.save(update_fields=['status'])
        # A cancellation timeline entry, so the customer sees it in their order history:
        order.order_timeline.create(
            status=Order.OrderStatus.CANCELLED,
            label='Order cancelled',
            time=timezone.now(),
            completed=True,
        )
        return order