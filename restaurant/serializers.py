# restaurants/serializers.py
from rest_framework import serializers
from .models import Restaurant, OpeningHours, RestaurantCategory


#  {#20b,7}
class RestaurantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCategory
        fields = ['id', 'name', 'slug', 'image', 'count']
        read_only_fields = ['id', 'slug', 'count']
        # count is a cached aggregate — never client-writable, recalculated by
        # backend logic (e.g. signal or scheduled task) as restaurants are added/removed


#  {#4f4,15}
class OpeningHoursSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display', read_only=True)

    class Meta:
        model = OpeningHours
        fields = ['id', 'day', 'day_display', 'open_time', 'close_time']
        read_only_fields = ['id']
        # 'restaurant' excluded — set server-side from the URL, same pattern as Address/PaymentMethod

    def validate(self, attrs):
        open_time = attrs.get('open_time')
        close_time = attrs.get('close_time')
        if open_time and close_time and open_time >= close_time:
            raise serializers.ValidationError("open_time must be earlier than close_time.")
        return attrs


#  {#fd6,17}
class RestaurantListSerializer(serializers.ModelSerializer):
    """Lightweight version for list/browse views — avoids over-fetching."""
    is_open_now = serializers.BooleanField(read_only=True)
    delivery_time = serializers.SerializerMethodField()
    categories = RestaurantCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id', 'restaurant_id', 'name', 'slug', 'logo', 'rating', 'review_count',
            'delivery_time', 'delivery_fee', 'minimum_order', 'categories',
            'is_open_now', 'is_temporarily_closed', 'is_featured', 'is_trending',
        ]
        read_only_fields = ['id', 'restaurant_id', 'slug', 'rating', 'review_count']

    def get_delivery_time(self, obj):
        return f"{obj.delivery_time_min}-{obj.delivery_time_max} min"


#  {#374,23}
class RestaurantDetailSerializer(serializers.ModelSerializer):
    """Fuller version for single-restaurant view — includes schedule and banner."""
    is_open_now = serializers.BooleanField(read_only=True)
    delivery_time = serializers.SerializerMethodField()
    categories = RestaurantCategorySerializer(many=True, read_only=True)
    opening_hours = OpeningHoursSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id', 'restaurant_id', 'name', 'slug', 'logo', 'banner',
            'rating', 'review_count', 'delivery_time', 'delivery_fee', 'minimum_order',
            'categories', 'opening_hours', 'is_open_now', 'is_temporarily_closed',
            'is_featured', 'is_trending', 'address', 'description', 'phone',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'restaurant_id', 'slug', 'rating', 'review_count',
            'created_at', 'updated_at',
        ]

    def get_delivery_time(self, obj):
        return f"{obj.delivery_time_min}-{obj.delivery_time_max} min"


class RestaurantWriteSerializer(serializers.ModelSerializer):
    """Separate serializer for create/update — accepts raw min/max minutes,
    category ids, and never touches rating/review_count."""
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=RestaurantCategory.objects.all()
    )

    class Meta:
        model = Restaurant
        fields = [
            'name', 'logo', 'banner', 'delivery_time_min', 'delivery_time_max',
            'delivery_fee', 'minimum_order', 'categories', 'is_temporarily_closed',
            'is_featured', 'is_trending', 'address', 'description', 'phone',
        ]

    def validate(self, attrs):
        min_t = attrs.get('delivery_time_min')
        max_t = attrs.get('delivery_time_max')
        if min_t is not None and max_t is not None and min_t > max_t:
            raise serializers.ValidationError(
                "Estimated minimum delivery time cannot be greater than Estimated maximum delivery time."
            )
        return attrs