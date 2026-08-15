# wallet/viewsets.py
from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Wallet, WalletTransaction
from ..serializers import WalletSerializer, WalletTransactionSerializer, WalletTopupSerializer
# from payments.services import create_payment_intent  # wire in once payments app exists


class WalletView(APIView):
    """GET /api/v1/wallet/ — the current user's own wallet."""

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        
        if wallet is None:
            return Response({'detail': 'No wallet found.'}, status=404)
        return Response(WalletSerializer(wallet).data)


class WalletTransactionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """GET /api/v1/wallet/transactions/"""
    serializer_class = WalletTransactionSerializer

    def get_queryset(self):
        return WalletTransaction.objects.filter(wallet__user=self.request.user).select_related('wallet')


class WalletTopupView(APIView):
    """POST /api/v1/wallet/topup/ — body: { amount }
    Creates a payment intent for the top-up amount. Does NOT credit the
    wallet directly — that only happens once the gateway's webhook confirms
    the payment succeeded, handled in the payments app (not yet built)."""

    def post(self, request):
        serializer = WalletTopupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']

        # Placeholder until the payments app exists:
        # payment_intent = create_payment_intent(amount=amount, purpose='wallet_topup')
        # return Response({'payment_intent_id': payment_intent['id'], 'client_secret': payment_intent['client_secret']})

        return Response(
            {'detail': 'Payment gateway integration not yet implemented.', 'amount': str(amount)},
            status=501,
        )