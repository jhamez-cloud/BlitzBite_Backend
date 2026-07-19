from rest_framework.routers import DefaultRouter
from .api.viewsets import PromotionViewset,CouponViewset

router = DefaultRouter()
router.register(r"promotions",PromotionViewset,basename="promotions")
router.register(r"coupons",CouponViewset,basename="coupons")

urlpatterns = router.urls