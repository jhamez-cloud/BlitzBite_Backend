# wallet/serializers.py
from rest_framework import serializers
from .models import Wallet, WalletTransaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'id', 'wallet_id', 'balance', 'currency',
            'promotional_credits', 'reward_points',
        ]
        read_only_fields = fields
        # Entirely read-only — balance/points only ever change through
        # create_wallet_transaction(), never via a direct PATCH.


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = ['id', 'type', 'description', 'amount', 'date', 'reference']
        read_only_fields = fields


class WalletTopupSerializer(serializers.Serializer):
    """POST /wallet/topup/ — body: { amount }
    Creates a payment intent for adding funds; wallet balance itself
    only updates once the gateway confirms payment via webhook —
    same rule as Order confirmation, never trust the client directly."""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)