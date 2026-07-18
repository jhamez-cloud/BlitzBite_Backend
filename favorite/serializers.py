from rest_framework import serializers
from .models import Favorite
from user.serializers import UserReadSerializer
from restaurant.serializers import RestaurantReadSerializer

class FavoriteReadSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(read_only=True)
    restaurant = RestaurantReadSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'