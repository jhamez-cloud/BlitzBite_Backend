from rest_framework import serializers
from .models import Favorite
from user.serializers import UserSerializer
from restaurant.serializers import RestaurantListSerializer

class FavoriteReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    restaurant = RestaurantListSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'