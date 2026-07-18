from rest_framework import serializers
from .models import MenuCategory,Addon,MenuItem
from restaurant.serializers import RestaurantWriteSerializer

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'

class AddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addon
        fields = '__all__'

class MenuItemReadSerializer(serializers.ModelSerializer):
    addon = AddonSerializer(many=True,read_only=True)
    category = MenuCategorySerializer(many=True,read_only=True)
    class Meta:
        model = MenuItem
        fields = '__all__'

class MenuItemWriteSerializer(serializers.ModelSerializer):
    restaurant = RestaurantWriteSerializer(many=True)
    category = MenuCategorySerializer(many=True)
    addon = AddonSerializer(many=True)
    class Meta:
        model = MenuItem
        fields = ['restaurant',
                  'category',
                  'addon',
                  'name',
                  'description',
                  'price',
                  'image',
                  'available',
                  'calories',
                  'is_popular'
                ]