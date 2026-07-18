from .api.viewsets import OrderViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"orders", OrderViewset, basename="orders")

urlpatterns = router.urls