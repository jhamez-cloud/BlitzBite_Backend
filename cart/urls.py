from rest_framework.routers import DefaultRouter
from .api.viewsets import CartItemViewset

router = DefaultRouter()
router.register(r"cart-items",CartItemViewset,basename="cart-items")

urlpatterns = router.urls