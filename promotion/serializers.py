# promotions/serializers.py
from rest_framework import serializers
from .models import Promotion, Coupon


class PromotionSerializer(serializers.ModelSerializer):
    is_valid_now = serializers.BooleanField(read_only=True)

    class Meta:
        model = Promotion
        fields = [
            'id', 'promotion_id', 'title', 'description', 'code', 'image',
            'discount_percentage', 'valid_until', 'is_active', 'is_valid_now',
            'background_color', 'text_color', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'promotion_id', 'created_at', 'updated_at']


class CouponSerializer(serializers.ModelSerializer):
    """Admin-facing CRUD — full field visibility, but usage counters
    are never client-writable, only advanced by the validate/apply flow."""
    is_exhausted = serializers.BooleanField(read_only=True)
    is_valid_now = serializers.BooleanField(read_only=True)

    class Meta:
        model = Coupon
        fields = [
            'id', 'coupon_id', 'code', 'description', 'discount_type',
            'discount_value', 'minimum_order', 'valid_until', 'max_uses',
            'used_count', 'active', 'is_exhausted', 'is_valid_now',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'coupon_id', 'used_count', 'created_at', 'updated_at']


class CouponValidateSerializer(serializers.Serializer):
    """POST /coupons/validate/ — body: { code, subtotal } → { valid, discount_amount, new_total }"""
    code = serializers.CharField()
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, attrs):
        code = attrs['code']
        subtotal = attrs['subtotal']

        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            raise serializers.ValidationError({'code': 'Coupon not found.'})

        if not coupon.is_valid_now:
            raise serializers.ValidationError({'code': 'This coupon is no longer valid.'})

        if subtotal < coupon.minimum_order:
            raise serializers.ValidationError({
                'subtotal': f'Order must be at least {coupon.minimum_order} to use this coupon.'
            })

        attrs['coupon'] = coupon
        return attrs

    def calculate_discount(self):
        coupon = self.validated_data['coupon']
        subtotal = self.validated_data['subtotal']

        if coupon.discount_type == Coupon.DiscountTypes.PERCENTAGE:
            discount = subtotal * (coupon.discount_value / 100)
        else:
            discount = coupon.discount_value

        discount = min(discount, subtotal)  # never discount below zero
        new_total = subtotal - discount

        return {
            'valid': True,
            'discount_amount': round(discount, 2),
            'new_total': round(new_total, 2),
        }