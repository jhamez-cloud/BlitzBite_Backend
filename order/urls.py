# orders/urls.py
from rest_framework.routers import DefaultRouter
from .api.viewsets import OrderViewSet

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = router.urls