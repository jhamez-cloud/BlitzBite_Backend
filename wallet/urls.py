from rest_framework.routers import DefaultRouter
from .api.viewsets import WalletViewset,WalletTransactionViewset

router = DefaultRouter()
router.register(r"wallets",WalletViewset,basename="wallets")
router.register(r"wallet-transactions",WalletTransactionViewset,basename="wallet-transactions")

urlpatterns = router.urls