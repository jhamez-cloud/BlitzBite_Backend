from rest_framework import serializers
from .models import Review
from user.serializers import UserSerializer
from restaurant.serializers import RestaurantListSerializer

class ReviewReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    restaurant = RestaurantListSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'


class ReviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['date']