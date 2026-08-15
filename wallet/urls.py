# wallet/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .api.viewsets import WalletView, WalletTransactionViewSet, WalletTopupView

router = DefaultRouter()
router.register(r"wallet/transactions", WalletTransactionViewSet, basename="wallet-transactions")

urlpatterns = router.urls + [
    path("wallet/", WalletView.as_view(), name="wallet-detail"),
    path("wallet/topup/", WalletTopupView.as_view(), name="wallet-topup"),
]