# reviews/serializers.py
from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Read-side — used for GET /restaurants/{id}/reviews/"""
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'user_avatar', 'rating', 'comment', 'date']
        read_only_fields = fields


class ReviewCreateSerializer(serializers.Serializer):
    """POST /restaurants/{id}/reviews/ — body: { order_id, rating, comment? }
    Not a ModelSerializer: creation goes through create_review(), which
    enforces ownership + delivered-status + one-review-per-order, and
    recalculates the restaurant's cached rating/review_count as a side effect."""
    order_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(required=False, allow_blank=True, allow_null=True)