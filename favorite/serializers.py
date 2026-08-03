# favorites/serializers.py
from rest_framework import serializers
from restaurant.models import Restaurant
from restaurant.serializers import RestaurantListSerializer
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    restaurant = RestaurantListSerializer(read_only=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(
        source='restaurant', queryset=Restaurant.objects.all(), write_only=True
    )

    class Meta:
        model = Favorite
        fields = ['id', 'restaurant', 'restaurant_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_restaurant_id(self, restaurant):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        if user and user.is_authenticated:
            if Favorite.objects.filter(user=user, restaurant=restaurant).exists():
                raise serializers.ValidationError(
                    "You have already favorited this restaurant."
                )
        return restaurant