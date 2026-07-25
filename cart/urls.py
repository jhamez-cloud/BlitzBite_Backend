# cart/urls.py
from rest_framework.routers import DefaultRouter
from .api.viewsets import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"cart/items", CartItemViewSet, basename="cart-items")

urlpatterns = router.urls