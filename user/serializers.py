from rest_framework import serializers
from .models import User, Address, PaymentMethod


class AddressSerializer(serializers.ModelSerializer):
    coordinates = serializers.ReadOnlyField()  # exposes the @property from the model

    class Meta:
        model = Address
        fields = [
            'id', 'label', 'address', 'latitude', 'longitude',
            'is_default', 'coordinates', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
        # 'user' deliberately excluded — set server-side from the URL, never from client input


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'type', 'label', 'details', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']

    # Only these keys are ever allowed to exist in `details`, and only these
    # per type. Anything else in the payload is silently stripped or rejected.
    ALLOWED_DETAIL_KEYS = {
    'credit card': {'brand', 'last4', 'exp_month', 'exp_year', 'gateway_token'},
    'debit card': {'brand', 'last4', 'exp_month', 'exp_year', 'gateway_token'},
    'paypal': {'email_masked', 'gateway_token'},
    'apple pay': {'gateway_token'},
    'google pay': {'gateway_token'},
    'bank transfer': {'bank_name', 'account_last4', 'gateway_token'},
    'mobile payment': {'provider', 'phone_number_masked', 'gateway_token'},
    'blitz wallet': set(),
    }

    def validate(self, attrs):
        pm_type = attrs.get('type')
        details = attrs.get('details', {})
        allowed = self.ALLOWED_DETAIL_KEYS.get(pm_type)

        if allowed is None:
            raise serializers.ValidationError({'type': f"Unverified details for payment method type: {pm_type}"})

        unexpected = set(details.keys()) - allowed
        if unexpected:
            raise serializers.ValidationError({
                'details': f"Unexpected fields for type '{pm_type}': {sorted(unexpected)}. "
                           f"Allowed fields: {sorted(allowed)}"
            })

        # Extra guard: last4 must actually look like 4 digits, not a full card number
        if 'last4' in details and not (isinstance(details['last4'], str) and details['last4'].isdigit() and len(details['last4']) == 4):
            raise serializers.ValidationError({'details': "'last4' must be exactly 4 digits."})

        return attrs

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone']

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    payment_methods = PaymentMethodSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone', 'avatar',
            'total_orders', 'total_spent', 'preferences',
            'date_joined', 'addresses', 'payment_methods',
        ]
        read_only_fields = [
            'id', 'total_orders', 'total_spent', 'date_joined',
        ]