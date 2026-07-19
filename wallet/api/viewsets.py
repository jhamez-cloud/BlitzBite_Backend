from config.viewsets import StandardViewset
from wallet.models import Wallet,WalletTransaction
from wallet.serializers import WalletSerializer,WalletTransactionSerializer

class WalletTransactionViewset(StandardViewset):
    queryset = WalletTransaction.objects.all()
    serializer_class = WalletTransactionSerializer

class WalletViewset(StandardViewset):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer