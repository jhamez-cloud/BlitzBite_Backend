# reviews/viewsets.py
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from order.models import Order
from ..models import Review
from ..serializers import ReviewSerializer, ReviewCreateSerializer
from ..services import create_review


class RestaurantReviewViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               viewsets.GenericViewSet):
    """Nested under restaurant: /restaurants/{restaurant_pk}/reviews/
    Only list + create — reviews aren't edited/deleted through this API,
    matching your spec's endpoint list (GET and POST only)."""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(
            restaurant_id=self.kwargs['restaurant_pk']
        ).select_related('user')

    def create(self, request, *args, **kwargs):
        input_serializer = ReviewCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        try:
            order = Order.objects.get(
                pk=data['order_id'], restaurant_id=self.kwargs['restaurant_pk']
            )
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found for this restaurant.'}, status=404)

        try:
            review = create_review(
                user=request.user,
                order=order,
                rating=data['rating'],
                comment=data.get('comment'),
            )
        except ValueError as e:
            return Response({'detail': str(e)}, status=400)

        return Response(ReviewSerializer(review).data, status=201)