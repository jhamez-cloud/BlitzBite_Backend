from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .api.viewsets import UserViewSet, AddressViewSet, PaymentMethodViewSet

#Main User Routes
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

#Nested User Routes
users_router = routers.NestedSimpleRouter(router, r"users", lookup="user")
users_router.register(r"addresses", AddressViewSet, basename="user-addresses")
users_router.register(r"payment-methods", PaymentMethodViewSet, basename="user-payment-methods")

urlpatterns = router.urls + users_router.urls