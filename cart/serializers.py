from rest_framework import serializers
from .models import Cart,CartItem
from user.serializers import UserReadSerializer
from menu.serializers import MenuItemReadSerializer,MenuItemWriteSerializer,AddonSerializer
from restaurant.models import Restaurant

class CartSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(read_only=True)
    total = serializers.ReadOnlyField(source='total')
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemReadSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    menu_item = MenuItemReadSerializer(read_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(read_only=True)
    selected_addons = AddonSerializer(many=True,read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'

class CartItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['name',
                  'cart',
                  'menu_item',
                  'restaurant',
                  'price',
                  'quantity',
                  'selected_addons',
                  'special_instructions'
                ]