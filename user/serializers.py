from rest_framework import serializers
from .models import User,Address,PaymentMethod


class AddressSeriailizer(serializers.ModelSerializer):
    coordinates = serializers.ReadOnlyField(source='coordinates')
    class Meta:
        model = Address
        fields = ['id', 'label', 'latitude', 'longitude', 'is_default']

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'type', 'label','details']

class UserReadSerializer(serializers.ModelSerializer):
    addresses = AddressSeriailizer(many=True)
    payment_methods = PaymentMethodSerializer(many=True)
    class Meta:
        model = User
        fields = "__all__"

class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','phone','name','avatar','preferences','addresses','payment_methods']