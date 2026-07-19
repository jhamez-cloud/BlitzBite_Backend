from config.viewsets import StandardViewset
from review.models import Review
from review.serializers import ReviewReadSerializer, ReviewWriteSerializer

class ReviewViewset(StandardViewset):
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReviewReadSerializer
        return ReviewWriteSerializer