from config.viewsets import StandardViewset
from promotion.models import Promotion,Coupon
from promotion.serializers import PromotionSerializer,CouponSerializer


class PromotionViewset(StandardViewset):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

class CouponViewset(StandardViewset):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer