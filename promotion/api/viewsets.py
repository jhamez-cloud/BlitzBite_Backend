# promotions/viewsets.py
from rest_framework.views import APIView
from rest_framework.response import Response
from config.viewsets import StandardViewset
from ..models import Promotion, Coupon
from ..serializers import PromotionSerializer, CouponSerializer, CouponValidateSerializer


class PromotionViewSet(StandardViewset):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class CouponViewSet(StandardViewset):
    """Admin-facing CRUD for managing coupons — will be staff-only once auth exists."""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class CouponValidateView(APIView):
    """POST /api/v1/coupons/validate/ — public-facing, used at checkout
    to preview a coupon's discount before actually placing the order."""

    def post(self, request):
        serializer = CouponValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.calculate_discount()
        return Response(result)