from rest_framework import serializers
from .models import OrdersTimeLineEntry,Order,OrderItem
from menu.serializers import MenuItemReadSerializer,AddonSerializer
from user.serializers import UserSerializer

class OrderTimelineEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersTimeLineEntry
        fields = ['status', 'label', 'time', 'completed']
        ignore = ['order']

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()
    menu_item = MenuItemReadSerializer()
    addons = AddonSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ['menu_item','name','quantity', 'price', 'addons', 'subtotal']

class OrderReadSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True,read_only=True)
    user = UserSerializer(read_only=True)
    subtotal = serializers.ReadOnlyField()
    class Meta:
        model = Order
        fields = '__all__'

class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id',
                  'restaurant',
                  'user',
                  'order_items',
                  'delivery_address',
                  'payment_method',
                  'external_payment_id',
                  'tip','discount',
                  'delivery_fee',
                  'status',
                  'estimated_delivery_time',
                  'courier'
                ]