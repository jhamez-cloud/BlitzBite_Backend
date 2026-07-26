# promotions/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .api.viewsets import PromotionViewSet, CouponViewSet, CouponValidateView

router = DefaultRouter()
router.register(r"promotions", PromotionViewSet, basename="promotions")
router.register(r"coupons", CouponViewSet, basename="coupons")

urlpatterns = router.urls + [
    path("coupons/validate/", CouponValidateView.as_view(), name="coupon-validate"),
]