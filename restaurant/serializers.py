from rest_framework import serializers
from .models import Restaurant,OpeningHours,RestaurantCategory

class OpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = '__all__'

class RestaurantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCategory
        fields = '__all__'

class RestaurantReadSerializer(serializers.ModelSerializer):
    opening_hours = OpeningHoursSerializer(many=True,read_only=True)
    categories = RestaurantCategorySerializer(many=True,read_only=True)
    class Meta:
        model = Restaurant
        fields = '__all__'

class RestaurantWriteSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True,queryset=RestaurantCategory.objects.all())
    class Meta:
        model = Restaurant
        fields = ["name",
                  "logo",
                  "banner",
                  "rating",
                  "review_count",
                  "delivery_time",
                  "delivery_fee",
                  "minimum_order",
                  "categories",
                  "is_open",
                  "is_featured",
                  "is_trending",
                  "address",
                  "description",
                  "opening_hours",
                  "phone"]