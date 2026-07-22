from rest_framework import serializers
from .models import Wallet,WalletTransaction
from user.serializers import UserSerializer

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = ['wallet_id']

class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = "__all__"
        read_only_fields = ['id']