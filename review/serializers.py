from rest_framework import serializers
from .models import Review
from user.serializers import UserReadSerializer
from restaurant.serializers import RestaurantReadSerializer

class ReviewReadSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(read_only=True)
    restaurant = RestaurantReadSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'


class ReviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['date']